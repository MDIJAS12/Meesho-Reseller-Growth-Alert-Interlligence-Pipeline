# Meesho Reseller Growth & Alert Intelligence Pipeline

An end-to-end, production-grade reseller growth intelligence and alerting pipeline for Meesho category operations. This repository automates monthly category revenue tracking, enforces statistical threshold classification with strict input guardrails, generates hallucination-free executive narratives using masked data privacy, and orchestrates an auditable agentic workflow.

---

## 1. Pipeline Architecture & Workflow Pattern Mapping

This system operationalizes a robust, multi-stage data-to-decision pipeline:

### Part 1: SQL Business Query Engine
- *Workflow: "Measure the Business in SQL Before Any Decision is Made"*.
- All financial aggregates, order metrics, and business dimensions are computed directly against the SQLite persistence layer (`meesho_reseller.db`) using pure SQL.
- Downstream logic consumes validated numeric outputs rather than raw transactional data.

### Part 2: Input Guardrails & Growth Engine
- *Workflow: "Validate Inputs, Classify Change, and Enforce Guardrails"*.
- Numerical changes are converted into explicit rules such as MoM %, tri-state threshold classification, and exact boundary escalation.
- Raw inputs pass strict type and schema checks before they are ingested by the decision engine.

### Part 3: Narrative Reporting
- *Workflow: "Turn Verified Metrics into Safe, Structured Business Narratives"*.
- Verified outputs are transformed into templated Context → Insight → Implication narratives with zero hallucinated figures.
- Reseller-sensitive information is masked so stakeholder-facing updates remain privacy-safe and auditable.

### Part 4: Agentic Workflow & Mock Runner
- *Workflow: "Intake → Validate → Compute → Rank → Draft and Hold for Review"*.
- Orchestrates Parts 1, 2, and 3 into an automated, guarded workflow.
- Incorporates an anti-flooding notification cap (top 3 alerts), isolates suppressed or escalated categories, and enforces a human-in-the-loop review gate before dispatch.

---

## 2. Repository Structure

```text
.
├── README.md                             # Pipeline documentation and execution guide
├── data/
│   ├── generate_dataset.py               # Deterministic seeded synthetic data generator
│   ├── resellers.csv                     # Reseller master dataset (24 rows)
│   ├── orders.csv                        # Order transaction logs (900 rows)
│   └── meesho_reseller.db                # SQLite transactional database
├── part1_sql/
│   ├── queries.sql                       # Standing SQL business queries
│   ├── query_run.py                      # SQL runner script exporting CSV deliverables
│   └── output/
│       ├── monthly_category_revenue.csv  # 15-row monthly category revenue feed
│       ├── region_revenue_orders.csv     # Regional revenue & order breakdown
│       ├── top_5_resellers.csv           # Top 5 spenders (> ₹50,000)
│       ├── zero_order_resellers.csv      # Unmatched zero-order reseller (RS024)
│       ├── count_star_vs_count_order_id.csv # Diagnostic query for RS024 outer join
│       ├── june_delivered_aov.csv        # June Delivered AOV (₹1,267.69)
│       └── README.md                     # Analysis of SQL queries and COUNT(*) behavior
├── part2_engine/
│   ├── growth_engine.py                  # MoM calculation, boundary classifier & guardrail validator
│   ├── test_growth_engine.py             # Given-When-Then unit test suite
│   └── fixtures/
│       ├── corrupted_feed.csv            # Malformed CSV fixture for input validation
│       └── monthly_category_revenue.csv  # Clean baseline revenue fixture
├── part3_narrative/
│   ├── prompt_pack.md                    # 4-part reusable narrative prompt template
│   ├── narrative_report.md               # Worked May/June narratives & chart justifications
│   └── masking.py                        # PII privacy masking & leak detection assertions
└── part4_agent/
    ├── agent_spec.md                     # 5-component agent architecture & safety guardrails
    └── mock_agent_runner.py              # End-to-end mock agent pipeline runner
```

---

## 3. How to Run Each Stage in Sequential Order

### Step 1: Regenerate Dataset (Part 1.1)
Generates the synthetic reseller and order transaction records seeded with `random.Random(42)`.
```bash
python3 data/generate_dataset.py
```
*Expected Output:* Creates `data/resellers.csv` (24 rows), `data/orders.csv` (900 rows), and `data/meesho_reseller.db`. Zero-order reseller: `RS024`.

### Step 2: Execute SQL Business Queries (Part 1.2)
Executes all five standing business queries and exports the deliverables into `part1_sql/output/`.
```bash
python3 part1_sql/query_run.py
```
*Key Deliverable:* Generates `part1_sql/output/monthly_category_revenue.csv` (15 rows matching ₹1,262,066.92 total revenue).

### Step 3: Run Engine Unit Tests (Part 2)
Runs the test suite testing MoM growth, tri-state threshold classification, exact boundary escalation, and input feed guardrails.
```bash
python3 -m unittest part2_engine/test_growth_engine.py
```
*Expected Output:* `Ran 4 tests in 0.001s: OK`.

### Step 4: Run Privacy Masking Tests (Part 3)
Validates reseller PII masking and ensures no raw reseller names leak into stakeholder-facing updates.
```bash
python3 part3_narrative/masking.py
```
*Expected Output:* `All Part 3 masking tests passed successfully!`.

### Step 5: Execute Mock Agent Runner (Part 4)
Runs the end-to-end agentic workflow over May (April $\rightarrow$ May), June (May $\rightarrow$ June), and a corrupted feed scenario.
```bash
python3 part4_agent/mock_agent_runner.py
```
*Key Behaviors Demonstrated:*
- **May Scenario**: Identifies 5 flagged categories; drafts top 3 by magnitude (`Ethnic Wear`, `Western Wear`, `Kids Wear`); suppresses remaining 2 (`Beauty & Personal Care`, `Home & Kitchen`).
- **June Scenario**: Identifies 4 flagged categories; drafts top 3 (`Ethnic Wear`, `Home & Kitchen`, `Kids Wear`); suppresses 1 (`Western Wear`); leaves unflagged category (`Beauty & Personal Care`) untouched.
- **Corrupted Feed Scenario**: Triggers an immediate **Hard Stop** on malformed input, returns exact line-level errors, and generates zero downstream drafts.

---

## 4. Official Python Standard Library Documentation Consulted

During the design and implementation of this pipeline, the following official Python standard library documentation was referenced:
- [`csv`](https://docs.python.org/3/library/csv.html) — `csv.DictReader`, `csv.DictWriter`, and line number tracking via `reader.line_num`.
- [`sqlite3`](https://docs.python.org/3/library/sqlite3.html) — Database connection management, cursor execution, and SQL aggregation.
- [`unittest`](https://docs.python.org/3/library/unittest.html) — Test case organization, assertion methods (`assertEqual`, `assertTrue`, `assertFalse`).
- [`pathlib`](https://docs.python.org/3/library/pathlib.html) — Cross-platform filesystem navigation and path resolution.
- [`json`](https://docs.python.org/3/library/json.html) — Formatting and serializing agent structured execution state.
- [`random`](https://docs.python.org/3/library/random.html) — Seeded pseudo-random generation with `random.Random(42)`.
