import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
import unittest
import csv
from pathlib import Path
from part2_engine.growth_engine import mom_growth, is_flagged, validate_feed

SCRIPT_DIR = Path(__file__).resolve().parent

class TestGrowthEngine(unittest.TestCase):

    def test_required_cases(self):
        # Test 1
        g1 = mom_growth(104520.77, 185107.61)
        self.assertEqual(g1, 77.1)
        self.assertEqual(is_flagged(g1), "flagged")

        # Test 2
        g2 = mom_growth(35542.11, 37559.07)
        self.assertEqual(g2, 5.67)
        self.assertEqual(is_flagged(g2), "not_flagged")

        # Test 3
        g3 = mom_growth(100000.0, 108000.0)
        self.assertEqual(g3, 8.0)
        self.assertEqual(is_flagged(g3), "escalate_exact_boundary")

    def test_corrupted_fixture(self):
        corrupted_path = SCRIPT_DIR / "fixtures" / "corrupted_feed.csv"
        is_valid, errors = validate_feed(str(corrupted_path))
        self.assertFalse(is_valid)
        expected_errors = [
            "line 3: negative revenue (-4200.0) for category=Western Wear",
            "line 4: missing category (month=July)",
            "line 6: missing revenue (category=Home & Kitchen)"
        ]
        self.assertEqual(errors, expected_errors)

    def test_valid_fixture(self):
        valid_path = SCRIPT_DIR / "fixtures" / "monthly_category_revenue.csv"
        is_valid, errors = validate_feed(str(valid_path))
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])

    def test_full_may_and_june_mom_tables(self):
        valid_path = SCRIPT_DIR / "fixtures" / "monthly_category_revenue.csv"
        data = {"April": {}, "May": {}, "June": {}}
        with open(valid_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data[row["month"]][row["category"]] = float(row["revenue"])

        # May vs April
        may_expected = {
            "Ethnic Wear": (77.1, "flagged"),
            "Western Wear": (-23.6, "flagged"),
            "Kids Wear": (-23.48, "flagged"),
            "Home & Kitchen": (-9.25, "flagged"),
            "Beauty & Personal Care": (-12.75, "flagged"),
        }
        for cat, (exp_g, exp_f) in may_expected.items():
            g = mom_growth(data["April"][cat], data["May"][cat])
            f = is_flagged(g)
            self.assertEqual(g, exp_g)
            self.assertEqual(f, exp_f)

        # June vs May
        june_expected = {
            "Ethnic Wear": (-58.74, "flagged"),
            "Western Wear": (11.97, "flagged"),
            "Kids Wear": (23.9, "flagged"),
            "Home & Kitchen": (42.59, "flagged"),
            "Beauty & Personal Care": (5.67, "not_flagged"),
        }
        for cat, (exp_g, exp_f) in june_expected.items():
            g = mom_growth(data["May"][cat], data["June"][cat])
            f = is_flagged(g)
            self.assertEqual(g, exp_g)
            self.assertEqual(f, exp_f)

if __name__ == "__main__":
    unittest.main()
