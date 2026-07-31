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


class ParseDate(unittest.TestCase):
    # every example string below occurs verbatim in the source table
    def test_full_date(self):
        self.assertEqual(gs.parse_date("21.VII.230", "start"),
                         {"start": "0230-07-21"})

    def test_double_date_same_month(self):
        self.assertEqual(gs.parse_date("28,29.XII.418", "start"),
                         {"start_elected": "0418-12-28",
                          "start_inaugurated": "0418-12-29"})

    def test_double_date_cross_month(self):
        self.assertEqual(gs.parse_date("12.X, 24.XI.642", "start"),
                         {"start_elected": "0642-10-12",
                          "start_inaugurated": "0642-11-24"})
        self.assertEqual(gs.parse_date("22.IV,30.VI.1073", "start"),
                         {"start_elected": "1073-04-22",
                          "start_inaugurated": "1073-06-30"})

    def test_double_date_cross_year(self):
        self.assertEqual(gs.parse_date("31.XII.532, 2.I.533", "start"),
                         {"start_elected": "0532-12-31",
                          "start_inaugurated": "0533-01-02"})

    def test_bare_year(self):
        self.assertEqual(gs.parse_date("68", "start"), {"start": "0068"})

    def test_year_alternates(self):
        self.assertEqual(gs.parse_date("64 or 67", "end"),
                         {"end_alternates": ["0064", "0067"]})

    def test_partial_year_month(self):
        self.assertEqual(gs.parse_date("...VIII.827", "start"),
                         {"start": "0827-08"})
        self.assertEqual(gs.parse_date("... VI.253", "start"),
                         {"start": "0253-06"})

    def test_partial_year_only(self):
        self.assertEqual(gs.parse_date("... 236", "start"), {"start": "0236"})
        self.assertEqual(gs.parse_date("...1032", "start"), {"start": "1032"})

    def test_irregular_forms_stay_raw_only(self):
        for raw in ("15 o 22 o 29.XII.384",   # Italian 'o'
                    "...XI or XII.872",        # month alternates
                    "... II-V.824",            # month range
                    "1,9,25.VIII.1471",        # triple date
                    "6 or 13.III.251",         # day alternates
                    "4.VII.964 or 965"):       # year alternates w/ full date
            self.assertEqual(gs.parse_date(raw, "start"), {}, raw)

    def test_double_dates_not_parsed_for_end_role(self):
        # elected/inaugurated semantics only apply to the beginning column
        self.assertEqual(gs.parse_date("28,29.XII.418", "end"), {})


class BuildPersons(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.persons = gs.build_persons(gs.extract_rows(HTML))
        cls.by_id = {p["id"]: p for p in cls.persons}

    def test_person_and_pontificate_counts(self):
        self.assertEqual(len(self.persons), 265)
        self.assertEqual(sum(len(p["pontificates"]) for p in self.persons), 267)

    def test_all_ids_unique_and_grammatical(self):
        ids = [p["id"] for p in self.persons]
        self.assertEqual(len(ids), len(set(ids)))
        for i in ids:
            self.assertTrue(gs.ID_RE.fullmatch(i), i)

    def test_peter(self):
        p = self.by_id["rp:peter"]
        self.assertIsNone(p["ordinal"])
        self.assertIsNone(p["roman"])
        self.assertEqual(p["cdcf_person"], "cdcf:person/pope-peter-i")
        self.assertIsNone(p["pontificates"][0]["start_raw"])
        self.assertEqual(p["pontificates"][0]["end_alternates"], ["0064", "0067"])

    def test_peter_secular_name_enrichment(self):
        p = self.by_id["rp:peter"]
        self.assertEqual(p["secular_name"], "Simon")
        self.assertIn("Mt 16:17", p["note"])
        self.assertIn("Christ's act", p["note"])

    def test_notes_only_on_documented_enrichments(self):
        self.assertEqual(sorted(q["id"] for q in self.persons if "note" in q),
                         ["rp:damasus-ii", "rp:formosus-i", "rp:peter",
                          "rp:theodore-i"])

    def test_sole_holders_get_ordinal_i(self):
        for pid in ("rp:francis-i", "rp:lando-i", "rp:linus-i", "rp:mark-i"):
            self.assertIn(pid, self.by_id)
        self.assertNotIn("rp:francis", self.by_id)

    def test_benedict_ix_one_person_three_pontificates(self):
        p = self.by_id["rp:benedict-ix"]
        self.assertEqual([q["number"] for q in p["pontificates"]], [145, 147, 150])
        self.assertEqual(p["ordinal"], 9)

    def test_aliases_carried(self):
        self.assertEqual(self.by_id["rp:anacletus-i"]["aliases"], ["Cletus"])
        self.assertEqual(self.by_id["rp:adeodatus-i"]["aliases"], ["Deusdedit"])
        self.assertIn("rp:adeodatus-ii", self.by_id)

    def test_numbering_skips_preserved(self):
        # there is no legitimate John XX: xix and xxi exist, xx must not
        self.assertIn("rp:john-xix", self.by_id)
        self.assertIn("rp:john-xxi", self.by_id)
        self.assertNotIn("rp:john-xx", self.by_id)

    def test_reigning_pope_open_ended(self):
        p = self.by_id["rp:leo-xiv"]
        self.assertEqual(p["ordinal"], 14)
        self.assertEqual(p["pontificates"][0]["number"], 267)
        self.assertIsNone(p["pontificates"][0]["end_raw"])
        self.assertEqual(p["pontificates"][0]["start_elected"], "2025-05-08")
        self.assertEqual(p["pontificates"][0]["start_inaugurated"], "2025-05-18")

    def test_modern_double_date(self):
        p = self.by_id["rp:francis-i"]
        pont = p["pontificates"][0]
        self.assertEqual(pont["start_raw"], "13,19.III.2013")
        self.assertEqual(pont["start_elected"], "2013-03-13")
        self.assertEqual(pont["start_inaugurated"], "2013-03-19")
        self.assertEqual(pont["end"], "2025-04-21")

    def test_cdcf_cross_reference(self):
        self.assertEqual(self.by_id["rp:leo-xiv"]["cdcf_person"],
                         "cdcf:person/pope-leo-xiv")
        self.assertEqual(self.by_id["rp:john-paul-ii"]["cdcf_person"],
                         "cdcf:person/pope-john-paul-ii")


class BirthCountry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.persons = gs.build_persons(gs.extract_rows(HTML))
        cls.by_id = {p["id"]: p for p in cls.persons}

    def test_every_record_has_the_field(self):
        for p in self.persons:
            self.assertIn("birth_country", p)

    def test_codes_are_alpha2_or_null(self):
        for p in self.persons:
            code = p["birth_country"]
            if code is not None:
                self.assertRegex(code, r"^[A-Z]{2}$")

    def test_modern_birthplaces(self):
        expected = {"rp:leo-xiv": "US", "rp:francis-i": "AR",
                    "rp:john-paul-ii": "PL", "rp:benedict-xvi": "DE",
                    "rp:adrian-vi": "NL", "rp:adrian-iv": "GB",
                    "rp:john-xxi": "PT", "rp:alexander-vi": "ES",
                    "rp:leo-xiii": "IT"}
        for pid, code in expected.items():
            self.assertEqual(self.by_id[pid]["birth_country"], code, pid)

    def test_regional_and_interpreted_birthplaces(self):
        expected = {"rp:victor-i": "TN",       # "Africa" -> Carthaginian heartland
                    "rp:caius-i": "HR",        # Dalmatia
                    "rp:gregory-iii": "SY",    # Syria
                    "rp:hilarius-i": "IT",     # Sardinia
                    "rp:liberius-i": "IT",     # "Romano"
                    "rp:john-xii": "IT",       # "Counts of Tusculum"
                    "rp:innocent-v": "FR",     # Savoy (Tarentaise)
                    "rp:martin-iv": "FR"}      # table: "France"
        for pid, code in expected.items():
            self.assertEqual(self.by_id[pid]["birth_country"], code, pid)

    def test_contested_or_nonplace_null_with_note(self):
        peter = self.by_id["rp:peter"]
        self.assertIsNone(peter["birth_country"])
        self.assertIn("contested", peter["note"])
        theodore = self.by_id["rp:theodore-i"]
        self.assertIsNone(theodore["birth_country"])
        self.assertIn("Jerusalem", theodore["note"])
        formosus = self.by_id["rp:formosus-i"]
        self.assertIsNone(formosus["birth_country"])
        self.assertIn("Portus", formosus["note"])

    def test_damasus_ii_bavaria_enrichment(self):
        p = self.by_id["rp:damasus-ii"]
        self.assertEqual(p["birth_country"], "DE")
        self.assertIn("Pildenau", p["note"])
        self.assertIn("natione Noricus", p["note"])

    def test_blank_birthplace_yields_null(self):
        self.assertIsNone(self.by_id["rp:benedict-ix"]["birth_country"])


class RenderMarkdown(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.persons = gs.build_persons(gs.extract_rows(HTML))
        cls.md = gs.render_markdown(cls.persons)
        cls.lines = cls.md.splitlines()

    def test_one_row_per_pontificate_in_succession_order(self):
        data_rows = [l for l in self.lines
                     if l.startswith("| ") and not l.startswith("| N ")
                     and not l.startswith("| ---")]
        self.assertEqual(len(data_rows), 267)
        numbers = [int(r.split("|")[1]) for r in data_rows]
        self.assertEqual(numbers, list(range(1, 268)))

    def test_first_and_last_rows(self):
        self.assertIn("| 1 | `rp:peter` | Peter |  | 64 or 67 | Simon "
                      "| Bethsaida of Galilee |  |", self.md)
        self.assertIn("| 267 | `rp:leo-xiv` | Leo XIV | 8,18.V.2025 |  "
                      "| Robert Francis Prevost | Chicago | US |", self.md)

    def test_intro_explains_country_column(self):
        self.assertIn("ISO 3166-1 alpha-2", self.md)

    def test_intro_explains_secular_name_column(self):
        self.assertIn("reverence for the Apostle", self.md)
        self.assertIn("John II", self.md)
        self.assertIn("Christ's act", self.md)

    def test_intro_explains_ordinal_convention(self):
        self.assertIn("only once a later pope takes the same name", self.md)
        self.assertIn("unlike labels", self.md)

    def test_benedict_ix_id_repeats_per_pontificate(self):
        self.assertEqual(self.md.count("`rp:benedict-ix`"), 3)

    def test_dates_are_verbatim_raw_strings(self):
        self.assertIn("| 266 | `rp:francis-i` | Francis | 13,19.III.2013 "
                      "| 21.IV.2025 |", self.md)

    def test_intro_states_counts_and_draft_status(self):
        self.assertIn("265 canonical IDs", self.md)
        self.assertIn("267 pontificates", self.md)
        self.assertIn("drafts pending committee review", self.md)


if __name__ == "__main__":
    unittest.main()
