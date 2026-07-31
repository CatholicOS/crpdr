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
