# Reusable Prompt Pack — Flagged Category Narrative

## Trigger

Start this prompt when a category's `is_flagged` result is `"flagged"`.

## Input list

The prompt requires these placeholder variables:

- `{category}` — category name
- `{previous_revenue}` — revenue for the previous month
- `{current_revenue}` — revenue for the current month
- `{mom_pct}` — month-over-month growth percentage
- `{month}` — current month
- `{prev_month}` — previous month
- `{reseller_alias}` — coded reseller alias, if a reseller is referenced

## Prompt

Write a concise stakeholder update for a regional manager about the flagged category using the Context → Insight → Implication structure.

Use these supplied values:
- Category: [{category}]
- Previous month: [{prev_month}]
- Current month: [{month}]
- Previous revenue: [{previous_revenue}]
- Current revenue: [{current_revenue}]
- MoM percentage: [{mom_pct}]

Rules:
1. In Context, state what is being measured and the comparison period.
2. In Insight, state the supplied MoM result and label it explicitly as a fact.
3. In Implication, give one specific and actionable next step.
4. If a possible cause is suggested, label it explicitly as a hypothesis because the supplied data does not prove causation.
5. Never state a number that is not one of the supplied placeholder values.
6. Do not invent additional metrics, causes, reseller names, or business facts.
7. 7. If a reseller is referenced, use only the supplied `{reseller_alias}` and never output a raw reseller name.

## Checklist

Before using the narrative, verify:

- [ ] **Check 1: Numeric Integrity**: Are all metrics in the narrative exact matches for the supplied inputs without hallucinated figures?
- [ ] **Check 2: Structural Verification**: Are Context, Insight, and Implication sections present and non-empty?
- [ ] **Check 3: Fact/Hypothesis Labeling**: Is every factual claim explicitly labeled `[Fact]` and speculative driver labeled `[Hypothesis]`?
- [ ] **Check 4: Privacy Masking**: Are raw reseller names completely excluded in favor of region + alias identifiers?