# CRPDR Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and publish the Common Roman Pontiff Data Repository (`CatholicOS/crpdr`): a seed registry of canonical `rp:` identifiers for the 265 Roman Pontiffs (267 pontificates), generated from a committed snapshot of the Holy See's reference table.

**Architecture:** A data-registry repo in the CECDR mold: a committed HTML source snapshot, a stdlib-only Python generator (`scripts/generate_seed.py`) with unit tests, the generated `data/pontiffs.json`, a schema proposal doc, and a README. No runtime code, no dependencies.

**Tech Stack:** Python 3 standard library only (`re`, `json`, `unittest`, `pathlib`). Git + `gh` CLI for publication.

## Global Constraints

- Repo root: `/home/johnrdorazio/development/CatholicOS_org/crpdr` (git repo already initialized on `main`; spec committed).
- ID scheme (spec §2): `rp:<name>-<roman>`; sole exception `rp:peter`. Lowercase ASCII only. Ordinal always present otherwise, including sole name-holders (`rp:francis-i`, `rp:lando-i`).
- Grammar every ID must match: `^rp:(peter|[a-z]+(-[a-z]+)*-[ivxlcdm]+)$`
- Entity model (spec §3): one record per **person** (265), pontificates as an attribute array (267 total). Benedict IX = one ID, three pontificates (table rows 145, 147, 150).
- Date rule (spec §4.1): `*_raw` fields verbatim always; parsed fields only where parsing is mechanical and unambiguous. Never silently normalize.
- Attribution: "curated by the **Catholic Engineering Task Force** of the [Catholic Digital Commons Foundation](https://github.com/CatholicOS)" — CETF, never a Project Committee (registries → CETF). Never "Catholic Open Source".
- Every public-facing doc states: **All IDs are drafts pending committee review.**
- License: Apache-2.0 (copy `LICENSE` from sibling repo `../cecdr/LICENSE`).
- Python: stdlib only; scripts runnable as `python3 scripts/generate_seed.py` from repo root.
- Source-snapshot policy: commit only the `<table id="holy-father">` element (factual table, ~40 KB), not the whole Vatican page (avoids republishing site chrome/scripts; keeps the copyright surface minimal, per CRMEDR precedent). Provenance recorded in `data/source/README.md`.
- Outward-facing steps (GitHub repo creation, upstream issues) have explicit **STOP** gates — confirm with the user before executing.

## Verified source facts (checked 2026-07-31 against the live page)

The plan's counts and test expectations were verified mechanically against the downloaded page:

- One `<table id="holy-father">`; 268 `<tr>` rows = 1 header + 267 data rows; 7 cells per row: `n | PAPAL NAME | BEGINNING PONTIFICATE | END PONTIFICATE | SECULAR NAME | BIRTH | CENTURY`.
- Only duplicated name: **Benedict IX**, rows 145, 147, 150 → 265 distinct persons.
- Three double-named rows: `Anacletus or Cletus` (row 3), `Miltiades or Melchiades` (row 44 area), `Deusdedit or Adeodatus  I` (row 68 — note double space in source; row 77 is `Adeodatus II`, so the canonical slug must be `adeodatus-i`).
- No non-ASCII characters in any papal name. 45 names lack a table ordinal (sole holders) — all get `-i` except Peter.
- Peter's row: BEGINNING empty, END `64 or 67`.
- Date-format census (start+end columns): `N.M.N`×306, `N,N.M.N`×66, `...M.N`(±space)×31, `N or N`×20, `N.M, N.M.N`/`N.M,N.M.N`×36, `N`×14, `N.M.N, N.M.N`×6, `... N`×3, plus ~30 rows of irregular forms (`15 o 22 o 29.XII.384`, `...XI or XII.872`, `... II-V.824`, `1,9,25.VIII.1471`, …) which stay raw-only.

---

### Task 1: Scaffold — license, gitignore, source snapshot with provenance

**Files:**
- Create: `LICENSE` (copied from `../cecdr/LICENSE`)
- Create: `.gitignore`
- Create: `data/source/holy-father-table.html`
- Create: `data/source/README.md`

**Interfaces:**
- Produces: `data/source/holy-father-table.html` — the verbatim `<table id="holy-father">…</table>` element; Task 2's `extract_rows()` parses exactly this file.

- [ ] **Step 1: Copy the Apache-2.0 license and add .gitignore**

```bash
cd /home/johnrdorazio/development/CatholicOS_org/crpdr
cp ../cecdr/LICENSE LICENSE
printf '__pycache__/\n*.pyc\n' > .gitignore
```

- [ ] **Step 2: Download the Vatican page and commit only the table element**

```bash
cd /home/johnrdorazio/development/CatholicOS_org/crpdr
mkdir -p data/source scripts docs
curl -sL 'https://www.vatican.va/content/vatican/en/holy-father.html' \
  -o /tmp/holy-father-full.html
python3 - <<'EOF'
import re
html = open('/tmp/holy-father-full.html', encoding='utf-8').read()
table = re.search(r'<table id="holy-father".*?</table>', html, re.S).group(0)
open('data/source/holy-father-table.html', 'w', encoding='utf-8').write(table + '\n')
print(len(table), 'bytes;', table.count('<tr'), 'rows')
EOF
```

Expected output: roughly `40000–90000 bytes; 268 rows` (268 = header + 267 data rows). If the row count is not 268, STOP — the live page changed since 2026-07-31; re-verify the "Verified source facts" section before continuing.

- [ ] **Step 3: Write the provenance note**

Create `data/source/README.md`:

```markdown
# Source snapshot

`holy-father-table.html` is the `<table id="holy-father">` element of the Holy
See's reference table of Roman Pontiffs:

- URL: https://www.vatican.va/content/vatican/en/holy-father.html
- Retrieved: 2026-07-31
- Extent: the table element only (268 `<tr>` rows: 1 header + 267 pontificates,
  Peter through Leo XIV). The surrounding page chrome is not included.

The table's factual content (names, dates, birthplaces) is the seed source of
truth for `data/pontiffs.json`; `scripts/generate_seed.py` parses this snapshot,
never the live site, so generation is reproducible and citable. To refresh the
snapshot (e.g. after a new pontificate begins), re-run the extraction documented
in `docs/superpowers/plans/2026-07-31-crpdr-implementation.md` Task 1 and update
the retrieval date here and in the script's `SOURCE_RETRIEVED` constant.
```

- [ ] **Step 4: Commit**

```bash
cd /home/johnrdorazio/development/CatholicOS_org/crpdr
git add LICENSE .gitignore data/source/
git commit -m "Scaffold: Apache-2.0 license, Vatican table snapshot with provenance

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 2: Row extraction and name handling (TDD)

**Files:**
- Create: `scripts/generate_seed.py` (module skeleton + `extract_rows`, `split_name`, `make_id`, `roman_to_int`)
- Test: `scripts/test_generate_seed.py`

**Interfaces:**
- Consumes: `data/source/holy-father-table.html` (Task 1).
- Produces (used by Tasks 3–4):
  - `extract_rows(html: str) -> list[list[str]]` — 267 rows × 7 cleaned cell strings (entities decoded to text, tags stripped, whitespace collapsed; empty cell → `""`).
  - `split_name(label: str) -> tuple[str, str | None, list[str]]` — `(name, roman_lowercase_or_None, aliases)`.
  - `make_id(name: str, roman: str | None) -> str` — `roman=None` yields a bare slug (used only for Peter).
  - `roman_to_int(s: str) -> int` — lowercase Roman numeral to integer.
  - `ALIASES: dict`, `ID_RE: re.Pattern`.

- [ ] **Step 1: Write the failing tests**

Create `scripts/test_generate_seed.py`:

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd /home/johnrdorazio/development/CatholicOS_org/crpdr
python3 -m unittest discover -s scripts -v
```

Expected: error — `ModuleNotFoundError: No module named 'generate_seed'`.

- [ ] **Step 3: Write the module with extraction and name handling**

Create `scripts/generate_seed.py`:

```python
#!/usr/bin/env python3
"""Generate the CRPDR seed registry from the committed snapshot of the Holy
See's reference table of Roman Pontiffs.

Source snapshot: data/source/holy-father-table.html — the
<table id="holy-father"> element of
https://www.vatican.va/content/vatican/en/holy-father.html
(see data/source/README.md for provenance). The generator parses the snapshot,
never the live site, so generation is reproducible.

Usage:
  python3 scripts/generate_seed.py [repo_root]
"""

import html as html_entities
import json
import re
import sys
from pathlib import Path

SOURCE_URL = "https://www.vatican.va/content/vatican/en/holy-father.html"
SOURCE_RETRIEVED = "2026-07-31"

ROMAN_MONTHS = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6,
    "VII": 7, "VIII": 8, "IX": 9, "X": 10, "XI": 11, "XII": 12,
}
ROMAN_CHARS = set("IVXLCDM")
ROMAN_VALUES = {"i": 1, "v": 5, "x": 10, "l": 50, "c": 100, "d": 500, "m": 1000}

# The ID grammar (docs/schema-proposal.md §grammar): every minted ID must match.
ID_RE = re.compile(r"^rp:(peter|[a-z]+(-[a-z]+)*-[ivxlcdm]+)$")

# Popes the source table lists under two names. Canonical name first (the
# committee lean recorded in docs/schema-proposal.md), alternate kept as an
# alias attribute. Adeodatus is canonical because the table itself numbers
# "Adeodatus II" (row 77) against this pope's "I".
ALIASES = {
    "Anacletus or Cletus": ("Anacletus", ["Cletus"]),
    "Miltiades or Melchiades": ("Miltiades", ["Melchiades"]),
    "Deusdedit or Adeodatus I": ("Adeodatus I", ["Deusdedit"]),
}


def roman_to_int(s):
    total = 0
    values = [ROMAN_VALUES[ch] for ch in s]
    for i, v in enumerate(values):
        total += -v if i + 1 < len(values) and values[i + 1] > v else v
    return total


def clean_cell(cell):
    text = re.sub(r"<[^>]+>", "", cell)
    text = html_entities.unescape(text)  # &nbsp; -> \xa0 (matched by \s), &amp; etc.
    return re.sub(r"\s+", " ", text).strip()


def extract_rows(html):
    """Return the 267 data rows, each a list of 7 cleaned cell strings."""
    table = re.search(r'<table id="holy-father".*?</table>', html, re.S).group(0)
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", table, re.S)
    return [
        [clean_cell(c) for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S)]
        for row in rows[1:]  # rows[0] is the column-header row
    ]


def split_name(label):
    """'Benedict IX' -> ('Benedict', 'ix', []); 'Francis' -> ('Francis', None, []).

    Aliased labels resolve through ALIASES first. Single-word names are never
    treated as ordinals (guards names like 'Mark')."""
    name, aliases = ALIASES.get(label, (label, []))
    parts = name.split()
    if len(parts) > 1 and set(parts[-1]) <= ROMAN_CHARS:
        return " ".join(parts[:-1]), parts[-1].lower(), aliases
    return name, None, aliases


def make_id(name, roman):
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return f"rp:{slug}" if roman is None else f"rp:{slug}-{roman}"
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd /home/johnrdorazio/development/CatholicOS_org/crpdr
python3 -m unittest discover -s scripts -v
```

Expected: all tests PASS (classes `ExtractRows`, `SplitName`, `MakeId`, `RomanToInt`).

- [ ] **Step 5: Commit**

```bash
cd /home/johnrdorazio/development/CatholicOS_org/crpdr
git add scripts/generate_seed.py scripts/test_generate_seed.py
git commit -m "Add table extraction and name/ID handling with tests

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: Date parsing (TDD)

**Files:**
- Modify: `scripts/generate_seed.py` (append `parse_date_iso`, `parse_date`)
- Modify: `scripts/test_generate_seed.py` (append `ParseDate` test class)

**Interfaces:**
- Produces: `parse_date(raw: str, role: str) -> dict` where `role` is `"start"` or `"end"`. Returns `{}` for formats not mechanically unambiguous (caller keeps only `*_raw`). Parsed keys: `{role}` (single ISO-ish value: `"0230-07-21"`, partial `"0827-08"`, or year `"0068"`), `{role}_alternates` (list of years), `{role}_elected` + `{role}_inaugurated` (double dates, start column only).

- [ ] **Step 1: Write the failing tests**

Append to `scripts/test_generate_seed.py` (before the `if __name__` block):

```python
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
```

- [ ] **Step 2: Run tests to verify the new class fails**

```bash
cd /home/johnrdorazio/development/CatholicOS_org/crpdr
python3 -m unittest discover -s scripts -v 2>&1 | tail -5
```

Expected: `AttributeError: module 'generate_seed' has no attribute 'parse_date'` (earlier classes still pass).

- [ ] **Step 3: Implement date parsing**

Append to `scripts/generate_seed.py` (after `make_id`):

```python
def parse_date_iso(day, month, year):
    return f"{int(year):04d}-{ROMAN_MONTHS[month]:02d}-{int(day):02d}"


def parse_date(raw, role):
    """Parse one table date string into fields prefixed by `role` ('start' or
    'end'). Returns {} for any format that is not mechanically unambiguous —
    the caller always keeps the verbatim string in {role}_raw, so nothing is
    lost (schema rule: parsed fields only where parsing is trivial).

    Double dates ('13,19.III.2013') are election and inauguration; that
    semantic belongs to the BEGINNING column only, so they parse only when
    role == 'start'."""
    def key(suffix=""):
        return f"{role}_{suffix}" if suffix else role

    m = re.fullmatch(r"(\d+)\.([IVX]+)\.(\d+)", raw)
    if m:
        return {key(): parse_date_iso(m.group(1), m.group(2), m.group(3))}
    if role == "start":
        m = re.fullmatch(r"(\d+),(\d+)\.([IVX]+)\.(\d+)", raw)
        if m:
            return {key("elected"): parse_date_iso(m.group(1), m.group(3), m.group(4)),
                    key("inaugurated"): parse_date_iso(m.group(2), m.group(3), m.group(4))}
        m = re.fullmatch(r"(\d+)\.([IVX]+), ?(\d+)\.([IVX]+)\.(\d+)", raw)
        if m:
            return {key("elected"): parse_date_iso(m.group(1), m.group(2), m.group(5)),
                    key("inaugurated"): parse_date_iso(m.group(3), m.group(4), m.group(5))}
        m = re.fullmatch(r"(\d+)\.([IVX]+)\.(\d+), ?(\d+)\.([IVX]+)\.(\d+)", raw)
        if m:
            return {key("elected"): parse_date_iso(m.group(1), m.group(2), m.group(3)),
                    key("inaugurated"): parse_date_iso(m.group(4), m.group(5), m.group(6))}
    m = re.fullmatch(r"(\d+)", raw)
    if m:
        return {key(): f"{int(raw):04d}"}
    m = re.fullmatch(r"(\d+) or (\d+)", raw)
    if m:
        return {key("alternates"): [f"{int(m.group(1)):04d}", f"{int(m.group(2)):04d}"]}
    m = re.fullmatch(r"\.\.\. ?([IVX]+)\.(\d+)", raw)
    if m:
        return {key(): f"{int(m.group(2)):04d}-{ROMAN_MONTHS[m.group(1)]:02d}"}
    m = re.fullmatch(r"\.\.\. ?(\d+)", raw)
    if m:
        return {key(): f"{int(m.group(1)):04d}"}
    return {}
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd /home/johnrdorazio/development/CatholicOS_org/crpdr
python3 -m unittest discover -s scripts -v
```

Expected: all tests PASS, including all `ParseDate` cases.

- [ ] **Step 5: Commit**

```bash
cd /home/johnrdorazio/development/CatholicOS_org/crpdr
git add scripts/generate_seed.py scripts/test_generate_seed.py
git commit -m "Add date parsing: unambiguous formats parsed, irregular kept raw-only

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 4: Person grouping, validation, and seed emission (TDD)

**Files:**
- Modify: `scripts/generate_seed.py` (append `build_persons`, `validate`, `main`)
- Modify: `scripts/test_generate_seed.py` (append `BuildPersons` test class)
- Create (generated): `data/pontiffs.json`

**Interfaces:**
- Consumes: `extract_rows`, `split_name`, `make_id`, `roman_to_int`, `parse_date`, `ID_RE` (Tasks 2–3).
- Produces: `build_persons(rows) -> list[dict]` (265 person records, spec §4 schema); `data/pontiffs.json` with top-level keys `$comment`, `id_scheme`, `source`, `person_count`, `pontificate_count`, `entries`.

- [ ] **Step 1: Write the failing tests**

Append to `scripts/test_generate_seed.py` (before the `if __name__` block):

```python
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
```

- [ ] **Step 2: Run tests to verify the new class fails**

```bash
cd /home/johnrdorazio/development/CatholicOS_org/crpdr
python3 -m unittest discover -s scripts -v 2>&1 | tail -5
```

Expected: `AttributeError: module 'generate_seed' has no attribute 'build_persons'`.

- [ ] **Step 3: Implement grouping, validation, and main**

Append to `scripts/generate_seed.py` (after `parse_date`):

```python
def build_persons(rows):
    """Fold the 267 pontificate rows into person records (one per pope).

    Ordinal rule (docs/schema-proposal.md): every ID carries a Roman-numeral
    ordinal, including sole holders of a name (forward stability) — except
    Peter, who is never styled with one."""
    persons = {}
    order = []
    for number, cells in enumerate(rows, 1):
        label = cells[1]
        name, roman, aliases = split_name(label)
        if name == "Peter" and roman is None:
            roman_final = None
        else:
            roman_final = roman or "i"
        pid = make_id(name, roman_final)
        pont = {"number": number,
                "start_raw": cells[2] or None,
                "end_raw": cells[3] or None}
        if cells[2]:
            pont.update(parse_date(cells[2], "start"))
        if cells[3]:
            pont.update(parse_date(cells[3], "end"))
        if pid in persons:
            persons[pid]["pontificates"].append(pont)
        else:
            persons[pid] = {
                "id": pid,
                "name": name,
                "ordinal": roman_to_int(roman_final) if roman_final else None,
                "roman": roman_final,
                "label_en": label,
                "aliases": aliases,
                "secular_name": cells[4] or None,
                "birthplace": cells[5] or None,
                "century": int(cells[6]) if cells[6] else None,
                "pontificates": [pont],
                # provisional for Peter: cdcf-uri-scheme §3.6.1 mandates the
                # ordinal; a Peter exception is proposed upstream
                "cdcf_person": ("cdcf:person/pope-peter-i" if pid == "rp:peter"
                                else "cdcf:person/pope-" + pid[len("rp:"):]),
            }
            order.append(pid)
    return [persons[p] for p in order]


def validate(persons, rows):
    ids = [p["id"] for p in persons]
    dupes = {i for i in ids if ids.count(i) > 1}
    assert not dupes, f"duplicate IDs: {dupes}"
    bad = [i for i in ids if not ID_RE.fullmatch(i)]
    assert not bad, f"IDs failing grammar: {bad}"
    total = sum(len(p["pontificates"]) for p in persons)
    assert total == len(rows), f"pontificate count {total} != row count {len(rows)}"


def main():
    repo_root = (Path(sys.argv[1]) if len(sys.argv) > 1
                 else Path(__file__).resolve().parent.parent)
    html = (repo_root / "data" / "source" / "holy-father-table.html"
            ).read_text(encoding="utf-8")
    rows = extract_rows(html)
    persons = build_persons(rows)
    validate(persons, rows)

    def has_parsed(pont, col):
        return any(k == col or (k.startswith(col + "_") and k != col + "_raw")
                   for k in pont)

    raw_only = sum(1 for p in persons for pont in p["pontificates"]
                   for col in ("start", "end")
                   if pont[col + "_raw"] and not has_parsed(pont, col))
    out = {
        "$comment": ("CRPDR seed registry: draft canonical IDs for the Roman "
                     "Pontiffs, generated from the Holy See's reference table "
                     "(see data/source/README.md). All IDs are drafts pending "
                     "committee review (docs/schema-proposal.md)."),
        "id_scheme": "rp:<name>-<roman> (sole exception: rp:peter)",
        "source": {"url": SOURCE_URL, "retrieved": SOURCE_RETRIEVED},
        "person_count": len(persons),
        "pontificate_count": len(rows),
        "entries": persons,
    }
    dest = repo_root / "data" / "pontiffs.json"
    dest.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8")
    print(f"wrote {dest}: {len(persons)} persons, {len(rows)} pontificates; "
          f"{raw_only} date strings kept raw-only")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd /home/johnrdorazio/development/CatholicOS_org/crpdr
python3 -m unittest discover -s scripts -v
```

Expected: all tests PASS.

- [ ] **Step 5: Generate the seed and eyeball it**

```bash
cd /home/johnrdorazio/development/CatholicOS_org/crpdr
python3 scripts/generate_seed.py
python3 -c "
import json
d = json.load(open('data/pontiffs.json'))
assert d['person_count'] == 265 and d['pontificate_count'] == 267
print(json.dumps(d['entries'][0], indent=2))          # Peter
print(json.dumps(d['entries'][-1], indent=2))         # Leo XIV
print([p['id'] for p in d['entries'] if p['id'].startswith('rp:benedict-ix')])
"
```

Expected: generator prints `wrote … 265 persons, 267 pontificates; N date strings kept raw-only` (N around 40); Peter and Leo XIV records match the schema in spec §4; exactly one `rp:benedict-ix`.

- [ ] **Step 6: Commit**

```bash
cd /home/johnrdorazio/development/CatholicOS_org/crpdr
git add scripts/generate_seed.py scripts/test_generate_seed.py data/pontiffs.json
git commit -m "Add person grouping and emit the 265-person seed registry

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 5: Schema proposal document

**Files:**
- Create: `docs/schema-proposal.md`

**Interfaces:**
- Consumes: the approved spec (`docs/superpowers/specs/2026-07-31-crpdr-design.md`) — the schema proposal is its public-facing distillation.
- Produces: the document the README links to.

- [ ] **Step 1: Write the document**

Create `docs/schema-proposal.md` with exactly this content:

````markdown
# CRPDR schema proposal

**Status: draft, pending committee review.** This document proposes the
identifier scheme and record schema for the Common Roman Pontiff Data
Repository and records the open questions the committee must decide.

## Identifier scheme

```
rp:<name>-<roman-ordinal>        (general case)
rp:peter                         (sole exception)
```

Examples: `rp:linus-i`, `rp:gregory-i`, `rp:john-paul-ii`, `rp:benedict-xvi`,
`rp:francis-i`, `rp:leo-xiv`, `rp:peter`.

### Rules

1. **English name slugs**, following the Holy See's English reference table,
   lowercased, hyphen-separated. English is the de-facto language of worldwide
   technology standards, and the authoritative seed table is itself in English.
   Latin and other-language labels belong in the data as attributes, not in
   the ID.
2. **Ordinal always present**, including names held by only one pope
   (`rp:francis-i`, `rp:lando-i`). Canonical IDs must be stable over time: if
   a future pope takes the name Francis, the label "Pope Francis" may become
   "Pope Francis I", but `rp:francis-i` never changes.
3. **The Peter exception.** `rp:peter` carries no ordinal: Peter is never
   styled "Pope Peter" nor "Peter I" in any usage, ecclesial or common. The ID
   remains stable regardless — a future Peter would be `rp:peter-ii`.
4. **No honorific in the slug.** The `rp:` prefix (*Romani Pontifices* /
   Roman Pontiffs) already scopes the namespace; repeating "pope-" inside
   every identifier would be redundant. The cdcf-uri-scheme's
   `pope-{name}-{roman}` form is carried as the `cdcf_person` cross-reference.
5. **Compound names hyphenate:** `rp:john-paul-i`, `rp:john-paul-ii`.
6. **Ordinals follow official numbering,** including historical skips (there
   is no legitimate John XX; the sequence passes from `rp:john-xix` to
   `rp:john-xxi`). CRPDR records the numbering as the Church uses it; it does
   not repair history.

### Grammar (ABNF, per RFC 5234)

```abnf
rp-id       = "rp:" pontiff-key
pontiff-key = "peter" / named-key
named-key   = name HYPHEN roman
name        = name-seg *(HYPHEN name-seg)
name-seg    = 1*ALPHA
roman       = 1*(%x69 / %x76 / %x78 / %x6C / %x63 / %x64 / %x6D)
                                        ; i v x l c d m, lowercase
ALPHA       = %x61-7A                   ; a-z, lowercase only
HYPHEN      = %x2D
```

The final hyphen-separated segment of a `named-key` is always the ordinal; no
papal name's final name-segment consists solely of Roman-numeral letters, so
the split is unambiguous. The `pontiff-key` production conforms to the `slug`
production of the [cdcf-uri-scheme](https://github.com/xudonglab/cdcf-uri-scheme)
ABNF (v0.3.0).

## Entity model: person, not pontificate

One record per **person**; reigns are an attribute array, not separate
identities. The forcing case is Benedict IX, who reigned three separate times
(1032–1044, 1045, 1047–1048; table rows 145, 147, 150) and is **one**
identifier, `rp:benedict-ix`, with three entries in `pontificates`. The
registry therefore holds 265 person records covering 267 pontificates.

## Record schema

```jsonc
{
  "id": "rp:benedict-ix",
  "name": "Benedict",              // English regnal name, no ordinal
  "ordinal": 9,                    // integer; null for rp:peter
  "roman": "ix",                   // lowercase Roman numeral; null for rp:peter
  "label_en": "Benedict IX",       // the source table's name, verbatim
  "aliases": [],                   // alternate names the table gives ("Cletus")
  "secular_name": "Theophylactus of Tusculum",  // null when the table is silent
  "birthplace": null,              // as given by the table
  "century": 11,                   // century of first accession, per the table
  "pontificates": [
    { "number": 145, "start_raw": "1032", "start": "1032",
      "end_raw": "1044", "end": "1044" },
    { "number": 147, "start_raw": "10.III.1045", "start": "1045-03-10",
      "end_raw": "1.V.1045", "end": "1045-05-01" },
    { "number": 150, "start_raw": "8.XI.1047", "start": "1047-11-08",
      "end_raw": "17.VII.1048", "end": "1048-07-17" }
  ],
  "cdcf_person": "cdcf:person/pope-benedict-ix"
}
```

### Date handling

The source table's dates are irregular and are never silently normalized:

- `*_raw` fields hold the source string verbatim and are the source of truth.
- Parsed fields exist only where parsing is mechanical and unambiguous:
  single dates (`21.VII.230` → `0230-07-21`), bare years (`68` → `0068`),
  year alternates (`64 or 67` → `["0064", "0067"]`), month partials
  (`...VIII.827` → `0827-08`), and — in the beginning column only — the
  election/inauguration double dates (`13,19.III.2013` →
  `start_elected: 2013-03-13`, `start_inaugurated: 2013-03-19`).
- Everything else (Italian "o" alternates, month ranges, triple dates) stays
  raw-only, pending open question n. 3 below.
- The reigning pope has `end_raw: null`.

## Relation to the cdcf-uri-scheme

The [cdcf-uri-scheme](https://github.com/xudonglab/cdcf-uri-scheme) (v0.3.0)
already legislates papal slugs: §3.2 unifies them to `pope-{name}-{roman}`
across the `cdcf:magisterium/` and `cdcf:person/` domains, and §3.6.1 mandates
the ordinal even for sole name-holders — the same forward-stability reasoning
as rule 2 above. CRPDR conforms to the spec's character set, English-name
choice, and ordinal-always rule; each record carries the spec's form as a
mechanical cross-reference (`rp:leo-xiv` ↔ `cdcf:person/pope-leo-xiv`).

**One deliberate divergence:** §3.6.1's blanket MUST implies `pope-peter-i`,
which matches no usage. CRPDR mints `rp:peter`; its `cdcf_person`
cross-reference is provisionally `cdcf:person/pope-peter-i` until the
exception proposed upstream is resolved.

## Open questions for the committee

1. **Antipopes.** Out of scope for the seed: the Holy See's table lists only
   legitimate pontiffs, and antipope lists have no single authoritative
   source. If the committee wants them, a discriminated segment (e.g.
   `rp:antipope-<name>-<roman>`) is sketched; numbering collisions with
   legitimate popes (Clement VII, Benedict XIII) make the discriminator
   mandatory.
2. **Double-named popes.** The table gives three: "Anacletus or Cletus",
   "Miltiades or Melchiades", "Deusdedit or Adeodatus I". The seed leans
   `rp:anacletus-i`, `rp:miltiades-i`, `rp:adeodatus-i` (the last forced by
   the table's own "Adeodatus II"), with the alternate name as an alias
   attribute. Committee to confirm.
3. **Date-uncertainty representation.** Is raw-plus-parsed sufficient, or is
   a structured uncertainty type
   ([EDTF](https://www.loc.gov/standards/datetime/)) warranted for the ~40
   irregular strings currently kept raw-only?
4. **The Peter divergence** from cdcf-uri-scheme §3.6.1, pending the upstream
   issue.
````

- [ ] **Step 2: Verify the document's claims against the generated data**

```bash
cd /home/johnrdorazio/development/CatholicOS_org/crpdr
python3 -c "
import json
d = json.load(open('data/pontiffs.json'))
by_id = {p['id']: p for p in d['entries']}
b9 = by_id['rp:benedict-ix']
assert [q['number'] for q in b9['pontificates']] == [145, 147, 150]
assert b9['pontificates'][1]['start'] == '1045-03-10'
assert by_id['rp:miltiades-i']['aliases'] == ['Melchiades']
print('schema-proposal claims verified')
"
```

Expected: `schema-proposal claims verified`.

- [ ] **Step 3: Commit**

```bash
cd /home/johnrdorazio/development/CatholicOS_org/crpdr
git add docs/schema-proposal.md
git commit -m "Add schema proposal with open questions for committee review

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 6: README

**Files:**
- Create: `README.md`

**Interfaces:**
- Consumes: `docs/schema-proposal.md` (Task 5), `data/pontiffs.json` (Task 4) — both are linked.

- [ ] **Step 1: Write the README**

Create `README.md` with exactly this content:

````markdown
# CRPDR

The home of the **Common Roman Pontiff Data Repository**, curated by the
**Catholic Engineering Task Force** of the
[Catholic Digital Commons Foundation](https://github.com/CatholicOS).

## What is CRPDR?

The Common Roman Pontiff Data Repository (CRPDR) provides a canonicalized list
of identifiers for the Roman Pontiffs, from Saint Peter to the reigning pope —
265 persons across 267 pontificates, seeded from the Holy See's own
[reference table of Roman Pontiffs](https://www.vatican.va/content/vatican/en/holy-father.html).

## Why?

Canonical papal identifiers are needed wherever Catholic data must reference a
pope unambiguously:

- **magisterial document attribution** — encyclicals, apostolic constitutions,
  and decrees are cited by their issuing pontiff (the
  [cdcf-uri-scheme](https://github.com/xudonglab/cdcf-uri-scheme) already
  builds `cdcf:magisterium/pope-leo-xiii/rerum-novarum`-style URIs on papal
  slugs; CRPDR provides the maintained registry behind them);
- **liturgical calendar data**, as served by the
  [Liturgical Calendar API](https://github.com/Liturgical-Calendar/LiturgicalCalendarAPI)
  (papal feasts, canonizations, calendar reforms);
- **Roman Martyrology cross-references** ([CRMEDR](https://github.com/CatholicOS/crmedr)):
  many eulogies commemorate popes;
- episcopal succession data, church-history datasets, and any application that
  must say *which* pope it means.

## The identifier scheme (draft)

```
rp:<name>-<roman-ordinal>        e.g. rp:leo-xiv, rp:john-paul-ii
rp:peter                         (sole exception: Peter bears no ordinal)
```

Every identifier carries its ordinal — including sole holders of a name
(`rp:francis-i`, `rp:lando-i`) — so that IDs never shift when a future pope
reuses a name: the *label* "Pope Francis" may one day become "Pope Francis I",
but the *identifier* is immutable. Identity belongs to the **person**, not the
pontificate: Benedict IX, who reigned three separate times, is one
`rp:benedict-ix` with three pontificate records. The full proposal — grammar,
date handling, the Peter exception, antipopes, and the open questions — is in
[docs/schema-proposal.md](docs/schema-proposal.md). **All IDs are drafts
pending committee review.**

## Repository contents

- [`data/pontiffs.json`](data/pontiffs.json) — the seed registry: 265 person
  records covering all 267 pontificates, each with its draft canonical ID,
  regnal name and ordinal, aliases, secular name, birthplace, dated
  pontificates (source strings verbatim plus parsed dates where unambiguous),
  and its `cdcf:person/` cross-reference.
- [`docs/schema-proposal.md`](docs/schema-proposal.md) — the proposed schema
  and the open questions for the committee.
- [`data/source/`](data/source/) — the committed snapshot of the Holy See's
  table (provenance in its README); the generator parses this snapshot, never
  the live site.
- [`scripts/generate_seed.py`](scripts/generate_seed.py) — regenerates the
  seed (`python3 scripts/generate_seed.py`); tests:
  `python3 -m unittest discover -s scripts`.

## Sources

The seed derives from the Holy See's reference table of Roman Pontiffs
(vatican.va). The registry records the succession as the Holy See presents it;
it takes no position on disputed historical questions.
````

- [ ] **Step 2: Verify links and run the full test suite one last time**

```bash
cd /home/johnrdorazio/development/CatholicOS_org/crpdr
ls data/pontiffs.json docs/schema-proposal.md data/source/README.md scripts/generate_seed.py
python3 -m unittest discover -s scripts
```

Expected: all four paths exist; all tests PASS.

- [ ] **Step 3: Commit**

```bash
cd /home/johnrdorazio/development/CatholicOS_org/crpdr
git add README.md
git commit -m "Add README with scheme summary and CETF attribution

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 7: Publish to GitHub — ⚠️ STOP: confirm with user first

Creating the public repo is outward-facing. **Ask the user to confirm** repo
creation under the `CatholicOS` org before running these steps.

**Files:** none (publication only).

- [ ] **Step 1: Confirm with the user** that `github.com/CatholicOS/crpdr` should be created as public.

- [ ] **Step 2: Create and push**

```bash
cd /home/johnrdorazio/development/CatholicOS_org/crpdr
gh repo create CatholicOS/crpdr --public \
  --description "Common Roman Pontiff Data Repository — canonical IDs for the Roman Pontiffs, curated by the Catholic Engineering Task Force of the CDCF" \
  --source . --push
```

Expected: repo created; `main` pushed.

- [ ] **Step 3: Verify**

```bash
gh repo view CatholicOS/crpdr --json name,description,visibility,defaultBranchRef
```

Expected: `"visibility": "PUBLIC"`, default branch `main`.

---

### Task 8: Upstream issues on xudonglab/cdcf-uri-scheme — ⚠️ STOP: confirm with user first

Filing issues on a third-party repo is outward-facing. **Show the user both
drafts and get explicit approval** (and any edits) before posting either.

**Files:** none (issue filing only). Draft bodies below are the deliverable to show the user.

- [ ] **Step 1: Show the user this draft for issue 1 and get approval**

Title: `§3.6.1 papal ordinal rule: the case of Peter`

Body:

```markdown
§3.6.1 requires every papal identifier to carry an ordinal suffix, "even for
names held by only one pope, to guarantee forward stability" — a rule we
fully agree with and have adopted in the CRPDR registry
(https://github.com/CatholicOS/crpdr).

One case seems to deserve an explicit carve-out: **Peter**. A strict reading
of the MUST yields `cdcf:person/pope-peter-i`, but Peter is never styled
"Pope Peter" nor "Peter I" in any ecclesial or common usage — including the
Holy See's own list of Roman Pontiffs, where every other repeated-name pope
carries an ordinal but Peter stands bare.

Forward stability is not endangered by an exception: if a future pope were
ever to take the name, he would be Peter II, and a bare `peter` slug would
remain untouched — the instability §3.6.1 guards against (a bare name later
acquiring an ordinal) cannot arise, because the first holder's bare styling
is itself the fixed historical usage.

Proposal: amend §3.6.1 with a single named exception, e.g.

> The sole exception is Peter, whose identifier is `pope-peter` (or `peter`):
> the first Roman Pontiff is never enumerated in ecclesial usage.

CRPDR currently mints `rp:peter` and carries `cdcf:person/pope-peter-i` as a
provisional cross-reference pending this issue's resolution; we're happy to
align with whatever the spec decides, and to submit a PR for the change if
that's welcome.
```

- [ ] **Step 2: Show the user this draft for issue 2 and get approval**

Title: `Registering an authoritative registry behind the papal slugs (CRPDR)`

Body:

```markdown
§3.2 [REV-02] unifies papal slugs to `pope-{name}-{roman}` across the
magisterium and person domains, and §3.6.1 fixes the ordinal rule — but the
set of valid `{name}-{roman}` values is currently open-ended, coined ad hoc
by implementers.

We've published CRPDR — the Common Roman Pontiff Data Repository
(https://github.com/CatholicOS/crpdr), curated by the Catholic Engineering
Task Force of the Catholic Digital Commons Foundation — which mints exactly
one canonical ID per pope (265 persons, 267 pontificates), seeded from the
Holy See's reference table, with each record carrying its `cdcf:person/`
form as a cross-reference (`rp:leo-xiv` ↔ `cdcf:person/pope-leo-xiv`).

Would the spec consider referencing a maintained registry as the source of
valid papal slugs (in §3.6.1 or an appendix), the way OSIS book abbreviations
are delegated in appendix A? That would make `cdcf:person/pope-*` and
magisterium issuer slugs mechanically checkable rather than convention-only.
Happy to submit a PR if that's the preferred route.
```

- [ ] **Step 3: File the approved issues**

```bash
gh issue create --repo xudonglab/cdcf-uri-scheme \
  --title '§3.6.1 papal ordinal rule: the case of Peter' \
  --body-file /tmp/crpdr-issue-1.md
gh issue create --repo xudonglab/cdcf-uri-scheme \
  --title 'Registering an authoritative registry behind the papal slugs (CRPDR)' \
  --body-file /tmp/crpdr-issue-2.md
```

(Write each approved body to the named temp file first; apply any edits the user requested.)

- [ ] **Step 4: Record the issue URLs**

Add the two issue URLs to `docs/schema-proposal.md` open questions n. 4 (replace "pending the upstream issue" with links), commit, and push:

```bash
cd /home/johnrdorazio/development/CatholicOS_org/crpdr
git add docs/schema-proposal.md
git commit -m "Link upstream cdcf-uri-scheme issues from the schema proposal

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
git push
```
