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

# Enrichments beyond the source table, applied after transcription and
# flagged in the emitted record's `note` field (docs/schema-proposal.md,
# open questions). The seed otherwise transcribes the table verbatim.
ENRICHMENTS = {
    "rp:peter": {
        "secular_name": "Simon",
        "note": ("secular_name is an enrichment: the source table leaves the "
                 "cell blank, presumably because Peter's renaming (Mt 16:17; "
                 "Jn 1:42) was Christ's act, not a regnal-name choice at "
                 "election — elsewhere the table fills the cell precisely "
                 "when the pre-election name differs."),
    },
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
    for pid, extra in ENRICHMENTS.items():
        persons[pid].update(extra)
    return [persons[p] for p in order]


def validate(persons, rows):
    ids = [p["id"] for p in persons]
    dupes = {i for i in ids if ids.count(i) > 1}
    assert not dupes, f"duplicate IDs: {dupes}"
    bad = [i for i in ids if not ID_RE.fullmatch(i)]
    assert not bad, f"IDs failing grammar: {bad}"
    total = sum(len(p["pontificates"]) for p in persons)
    assert total == len(rows), f"pontificate count {total} != row count {len(rows)}"


def render_markdown(persons):
    """Render the registry as a human-readable markdown table, one row per
    pontificate in succession order (so a pope with multiple pontificates
    repeats his ID). Dates are the source table's strings verbatim; the
    parsed forms live in data/pontiffs.json."""
    total = sum(len(p["pontificates"]) for p in persons)
    rows = sorted(((pont["number"], p, pont)
                   for p in persons for pont in p["pontificates"]),
                  key=lambda row: row[0])
    lines = [
        "# Roman Pontiffs",
        "",
        f"{len(persons)} canonical IDs covering the {total} pontificates of "
        "the Holy See's [reference table of Roman Pontiffs]"
        f"({SOURCE_URL}), from Peter to the reigning pope. One row per "
        "pontificate, in succession order: `N` is the succession number in "
        "the source table, so a pope with multiple pontificates (Benedict IX) "
        "repeats his ID. Dates are the source table's strings verbatim — the "
        "parsed forms are in [`data/pontiffs.json`](../data/pontiffs.json). "
        "All IDs are drafts pending committee review "
        "([schema proposal](../docs/schema-proposal.md)).",
        "",
        "The `Secular name` column follows the source table's own logic: it "
        "is filled only when the pre-election name differs from the papal "
        "name — first at n. 56 (John II, born Mercurio, 533, the first pope "
        "to change his name) — and for every pope from the eleventh century "
        "onward, once taking a regnal name had become the custom and the "
        "column also records the family name. A blank therefore means the "
        "pope reigned under his own name, not that the name is unknown. Two "
        "popes born Pietro — John XIV (n. 136) and Sergius IV (n. 142) — "
        "changed their names out of reverence for the Apostle; no pope has "
        "ever taken the name Peter. Peter's own secular name, Simon "
        "(Mt 16:17; Jn 1:42), is the registry's one enrichment beyond the "
        "table, which leaves that cell blank — presumably because his "
        "renaming was Christ's act, not a regnal-name choice at election.",
        "",
        "| N | ID | Papal name | Beginning of pontificate "
        "| End of pontificate | Secular name | Birth |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for number, p, pont in rows:
        lines.append("| {} | `{}` | {} | {} | {} | {} | {} |".format(
            number, p["id"], p["label_en"],
            pont["start_raw"] or "", pont["end_raw"] or "",
            p["secular_name"] or "", p["birthplace"] or ""))
    return "\n".join(lines) + "\n"


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
    md_dest = repo_root / "registry" / "pontiffs.md"
    md_dest.parent.mkdir(exist_ok=True)
    md_dest.write_text(render_markdown(persons), encoding="utf-8")
    print(f"wrote {dest} and {md_dest}: {len(persons)} persons, "
          f"{len(rows)} pontificates; {raw_only} date strings kept raw-only")


if __name__ == "__main__":
    main()
