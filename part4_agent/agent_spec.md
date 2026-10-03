# Part 4 — Agent Specification: Meesho Reseller Growth Alert Agent

## 1. Five Core Components of the Agentic System

### Goal
Keep Meesho category managers informed of any category whose month-on-month revenue moves beyond the 8% threshold, with a human approving every message before it goes out.

### Tools
The agent uses the following deterministic, offline tools:
- `validate_feed(csv_path: str) -> tuple[bool, list[str]]`: Validates the monthly revenue feed for structural integrity, missing values, non-numeric strings, and negative revenues before processing.
- `mom_growth(previous: float, current: float) -> float`: Calculates month-on-month percentage growth rounded to two decimal places.
- `is_flagged(mom_pct: float, threshold: float = 8.0) -> str`: Tri-state classifier returning `"flagged"` (magnitude > threshold), `"not_flagged"` (magnitude < threshold), or `"escalate_exact_boundary"` (magnitude == threshold).
- `_build_narrative(...)`: Offline prompt-pack template filler that constructs Context → Insight → Implication drafts using only verified numbers.

### Memory / State
The agent maintains state between execution cycles:
- Baseline revenue figures per category from the previous reporting month.
- Current month revenue figures per category.
- Evaluated category classifications across runs (`flagged_categories`, `suppressed_categories`, `escalated_categories`).

### Planner (Ordered Subtasks)
The agent executes an ordered sequence of 8 subtasks:
1. Load the monthly revenue feed and execute `validate_feed`.
2. If invalid, trigger a **Hard Stop** and surface validation errors immediately without further computation.
3. If valid, compute `mom_growth` for every category against the baseline previous month.
4. Run `is_flagged` on every category against the 8.0% threshold.
5. Sort flagged categories by absolute growth magnitude `abs(mom_pct)` descending.
6. Draft a stakeholder narrative (via Part 3 template) for at most the top 3 categories by magnitude to prevent notification flooding.
7. Log any remaining flagged categories beyond the top 3 into `suppressed_categories` (marked for manual review without message drafting).
7b. Separately log any category whose result is `"escalate_exact_boundary"` into `escalated_categories` without drafting a message.
8. Emit a single structured JSON response object capturing execution status, errors, drafts, suppressed categories, escalated categories, and action taken.

### Feedback Loop
Before any drafted notification is dispatched to stakeholders, it enters an explicit human-approval checkpoint. In this mock runner, the human-in-the-loop gate is represented by setting `action_taken = "drafted_and_held_for_approval"`. No external communication (email, webhook, or Slack) is ever dispatched autonomously.

---

## 2. Guardrails

- **Input Guardrail**: The feed must pass `validate_feed` with zero errors. Any schema deviation, missing value, non-numeric revenue, or negative revenue results in an immediate abort before any business logic executes.
- **Action Guardrail**: The agent is strictly constrained to drafting. Messages are permanently held in a review queue (`drafted_and_held_for_approval`) until authorized by a category operations lead.
- **Output Guardrail**: Strict numeric traceability. Every number appearing in a drafted message originates directly from verified Part 1 SQL aggregations or Part 2 engine computations. Zero synthetic or hallucinated numbers are permitted.

---

## 3. Stopping Conditions

- **Success Stopping Condition**: The agent completes execution when all categories have been classified, narrative drafts are produced for at most the top 3 flagged categories (or zero drafts if no category breached the 8.0% threshold), suppressed and escalated categories are logged, and `action_taken = "drafted_and_held_for_approval"`.
- **Error Stopping Condition (Hard Stop)**: If `validate_feed` returns `False`, execution immediately halts with `validation_status = "invalid"` and `action_taken = "hard_stop"`. No MoM computations or drafting are attempted, and the exact validation errors are returned to the caller.

---

## 4. Agent-Level Acceptance Specifications (Given-When-Then)

### Spec 1: High-Growth Category Alerting
- **GIVEN** April→May Ethnic Wear revenue increases from ₹104,520.77 to ₹185,107.61,
- **WHEN** the agent processes the May revenue feed,
- **THEN** it computes MoM growth as `77.1%`, classifies the category as `flagged`, drafts a Context → Insight → Implication alert, and ranks it as the top priority.

### Spec 2: Sub-Threshold Stability (Not Flagged)
- **GIVEN** May→June Beauty & Personal Care revenue moves from ₹35,542.11 to ₹37,559.07,
- **WHEN** the agent processes the June revenue feed,
- **THEN** it computes MoM growth as `5.67%`, classifies the category as `not_flagged`, and does not include it in either `flagged_categories` or `suppressed_categories`.

### Spec 3: Exact Boundary Escalation
- **GIVEN** a synthetic baseline of ₹100,000.00 and current revenue of ₹108,000.00 (exactly 8.0% growth),
- **WHEN** the agent evaluates the category against the threshold boundary,
- **THEN** it flags the category as `escalate_exact_boundary`, adds it to `escalated_categories`, and does not auto-draft an alert.

### Spec 4: Input Corruption Hard Stop
- **GIVEN** a corrupted revenue feed containing negative revenue on line 3, missing category on line 4, and missing revenue on line 6,
- **WHEN** the agent executes its intake validation phase,
- **THEN** it immediately triggers a Hard Stop, sets `action_taken = "hard_stop"`, leaves `flagged_categories` and `suppressed_categories` empty, and surfaces the 3 exact line-level error strings.
