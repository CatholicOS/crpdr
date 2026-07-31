"""Unit tests for generate_seed.py. Run from the repo root:

  python3 -m unittest discover -s scripts -v
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_seed as gs

REPO = Path(__file__).resolve().parent.parent
HTML = (REPO / "data" / "source" / "holy-father-table.html").read_text(encoding="utf-8")


class ExtractRows(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = gs.extract_rows(HTML)

    def test_row_count(self):
        self.assertEqual(len(self.rows), 267)

    def test_every_row_has_seven_cells(self):
        for row in self.rows:
            self.assertEqual(len(row), 7)

    def test_first_and_last_rows(self):
        self.assertEqual(self.rows[0][1], "Peter")
        self.assertEqual(self.rows[266][1], "Leo XIV")

    def test_peter_row_dates(self):
        self.assertEqual(self.rows[0][2], "")          # no beginning date
        self.assertEqual(self.rows[0][3], "64 or 67")  # end of pontificate

    def test_benedict_ix_occupies_rows_145_147_150(self):
        nums = [i for i, r in enumerate(self.rows, 1) if r[1] == "Benedict IX"]
        self.assertEqual(nums, [145, 147, 150])

    def test_double_space_normalized(self):
        names = [r[1] for r in self.rows]
        self.assertIn("Deusdedit or Adeodatus I", names)


class SplitName(unittest.TestCase):
    def test_name_with_ordinal(self):
        self.assertEqual(gs.split_name("Benedict IX"), ("Benedict", "ix", []))

    def test_sole_holder_no_table_ordinal(self):
        self.assertEqual(gs.split_name("Francis"), ("Francis", None, []))

    def test_compound_name(self):
        self.assertEqual(gs.split_name("John Paul II"), ("John Paul", "ii", []))

    def test_mark_is_not_an_ordinal(self):
        # single-word names are never treated as Roman numerals
        self.assertEqual(gs.split_name("Mark"), ("Mark", None, []))

    def test_aliased_names(self):
        self.assertEqual(gs.split_name("Anacletus or Cletus"),
                         ("Anacletus", None, ["Cletus"]))
        self.assertEqual(gs.split_name("Miltiades or Melchiades"),
                         ("Miltiades", None, ["Melchiades"]))
        self.assertEqual(gs.split_name("Deusdedit or Adeodatus I"),
                         ("Adeodatus", "i", ["Deusdedit"]))


class MakeId(unittest.TestCase):
    def test_ordinary(self):
        self.assertEqual(gs.make_id("Benedict", "xvi"), "rp:benedict-xvi")

    def test_compound(self):
        self.assertEqual(gs.make_id("John Paul", "ii"), "rp:john-paul-ii")

    def test_peter_bare(self):
        self.assertEqual(gs.make_id("Peter", None), "rp:peter")

    def test_ids_match_grammar(self):
        for i in ("rp:peter", "rp:john-paul-ii", "rp:lando-i", "rp:leo-xiv"):
            self.assertTrue(gs.ID_RE.fullmatch(i), i)
        for i in ("rp:francis", "rp:Pope-Leo-XIV", "rp:leo-", "leo-xiv"):
            self.assertFalse(gs.ID_RE.fullmatch(i), i)


class RomanToInt(unittest.TestCase):
    def test_values(self):
        for roman, value in (("i", 1), ("iv", 4), ("ix", 9), ("xiv", 14),
                             ("xvi", 16), ("xix", 19), ("xxiii", 23)):
            self.assertEqual(gs.roman_to_int(roman), value)


if __name__ == "__main__":
    unittest.main()
