import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
import csv
from pathlib import Path

# Direct import and reuse of Part 2 functions
from part2_engine.growth_engine import validate_feed, mom_growth, is_flagged

MONTH_SEQ = ["April", "May", "June", "July", "August", "September", "October", "November", "December"]

def _get_prev_month(month: str) -> str:
    if month in MONTH_SEQ:
        idx = MONTH_SEQ.index(month)
        if idx > 0:
            return MONTH_SEQ[idx - 1]
    return "Previous Month"

def _load_revenues(csv_path: str, target_month: str = None) -> dict[str, float]:
    revenues = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if target_month and "month" in row and row["month"]:
                if row["month"].strip() != target_month:
                    continue
            cat = row["category"].strip()
            rev = float(row["revenue"].strip())
            revenues[cat] = rev
    return revenues

def _build_narrative(category: str, prev_rev: float, curr_rev: float, mom_pct: float, month: str, prev_month: str) -> str:
    direction = "growth surge" if mom_pct > 0 else "revenue contraction"
    abs_g = abs(mom_pct)
    if mom_pct > 0:
        hyp = f"[Hypothesis] Growth surge in {category} during {month} was driven by increased reseller catalog adoption and seasonal promotional campaigns."
        rec = f"Recommendation: Expand inventory buffer for top {category} suppliers and secure fulfillment capacity."
    else:
        hyp = f"[Hypothesis] Revenue contraction in {category} during {month} resulted from post-promotional demand fatigue or temporary catalog stockouts."
        rec = f"Recommendation: Conduct an immediate supplier inventory audit for {category} and issue reseller catalog incentives."

    return (
        f"### Category Performance Alert: {category} ({month} 2026)\n\n"
        f"**Context**:\n"
        f"[Fact] Performance evaluation for category '{category}' comparing {prev_month} 2026 to {month} 2026. "
        f"[Fact] Baseline revenue in {prev_month} was INR {prev_rev:,.2f}, while revenue in {month} reached INR {curr_rev:,.2f}.\n\n"
        f"**Insight**:\n"
        f"[Fact] Category '{category}' recorded a month-on-month revenue change of {mom_pct}% (a {direction} of {abs_g}%). "
        f"[Fact] This shift exceeds the alert threshold of 8.0% and is classified as flagged.\n\n"
        f"**Implication**:\n"
        f"{hyp}\n"
        f"{rec}"
    )

def run(month: str, previous_month_csv: str, current_month_csv: str) -> dict:
    # 1. Load & validate current feed
    is_valid, validation_errors = validate_feed(current_month_csv)

    # 2. Hard Stop if invalid
    if not is_valid:
        return {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": validation_errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop"
        }

    # 3. Load category revenues
    prev_month_name = _get_prev_month(month)
    prev_revs = _load_revenues(previous_month_csv, target_month=prev_month_name)
    if not prev_revs:
        prev_revs = _load_revenues(previous_month_csv)

    curr_revs = _load_revenues(current_month_csv, target_month=month)
    if not curr_revs:
        curr_revs = _load_revenues(current_month_csv)

    flagged_pool = []
    escalated_categories = []

    # 4 & 5. Calculate MoM and classify
    for cat, curr_rev in curr_revs.items():
        if cat in prev_revs:
            prev_rev = prev_revs[cat]
            growth = mom_growth(prev_rev, curr_rev)
            flag_status = is_flagged(growth)

            cat_item = {
                "category": cat,
                "mom_pct": growth,
                "previous_revenue": prev_rev,
                "current_revenue": curr_rev,
            }

            if flag_status == "flagged":
                flagged_pool.append(cat_item)
            elif flag_status == "escalate_exact_boundary":
                escalated_categories.append(cat)

    # 6. Sort flagged categories by abs(mom_pct) descending
    flagged_pool.sort(key=lambda x: abs(x["mom_pct"]), reverse=True)

    # 7 & 8. Draft top 3 and suppress remaining
    flagged_categories = []
    suppressed_categories = []

    for idx, item in enumerate(flagged_pool):
        if idx < 3:
            msg = _build_narrative(
                category=item["category"],
                prev_rev=item["previous_revenue"],
                curr_rev=item["current_revenue"],
                mom_pct=item["mom_pct"],
                month=month,
                prev_month=prev_month_name
            )
            draft = {
                "category": item["category"],
                "mom_pct": item["mom_pct"],
                "previous_revenue": item["previous_revenue"],
                "current_revenue": item["current_revenue"],
                "drafted": True,
                "message": msg
            }
            flagged_categories.append(draft)
        else:
            suppressed_categories.append(item["category"])

    # 9 & 10. Emit JSON object
    return {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": flagged_categories,
        "suppressed_categories": suppressed_categories,
        "escalated_categories": escalated_categories,
        "action_taken": "drafted_and_held_for_approval"
    }



if __name__ == "__main__":
    import json
    rev_csv = str(ROOT_DIR / "part1_sql" / "output" / "monthly_category_revenue.csv")
    corr_csv = str(ROOT_DIR / "part2_engine" / "fixtures" / "corrupted_feed.csv")

    print("=== MAY SCENARIO ===")
    may_out = run("May", rev_csv, rev_csv)
    print(json.dumps(may_out, indent=2))

    print("\n=== JUNE SCENARIO ===")
    june_out = run("June", rev_csv, rev_csv)
    print(json.dumps(june_out, indent=2))

    print("\n=== CORRUPTED FEED SCENARIO ===")
    corr_out = run("July", rev_csv, corr_csv)
    print(json.dumps(corr_out, indent=2))
