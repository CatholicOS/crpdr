# CRPDR — Common Roman Pontiff Data Repository: Design

**Date:** 2026-07-31
**Status:** Approved design, pending implementation
**Repository:** `CatholicOS/crpdr`
**Curation:** Catholic Engineering Task Force (CETF) of the Catholic Digital Commons Foundation (CDCF)
**License:** Apache-2.0

## 1. Purpose

CRPDR provides canonical, stable identifiers for the Roman Pontiffs, from Saint Peter
to the reigning pope (currently Leo XIV), for use wherever Catholic data must reference
a pope unambiguously: magisterial document attribution (encyclicals, constitutions,
decrees), liturgical calendar data, martyrology cross-references, episcopal succession
data, and historical datasets.

The seed source is the Holy See's own reference table of Roman Pontiffs:
<https://www.vatican.va/content/vatican/en/holy-father.html> (267 numbered
pontificates, Peter through Leo XIV).

## 2. Identifier scheme

```
rp:<name>-<roman-ordinal>        (general case)
rp:peter                         (sole exception)
```

Examples: `rp:linus-i`, `rp:gregory-i`, `rp:john-paul-ii`, `rp:benedict-xvi`,
`rp:francis-i`, `rp:leo-xiv`, `rp:peter`.

### 2.1 Rules

1. **English name slugs.** Names follow the Vatican reference table's English page,
   lowercased, diacritics stripped, spaces replaced by hyphens. English is the
   de-facto language of worldwide technology standards, and the authoritative seed
   table is itself in English. (Latin forms — `papa-linus` etc. — were considered
   and rejected; Latin labels belong in the data as attributes, not in the ID.)
2. **Ordinal always present.** Every identifier carries a lowercase Roman-numeral
   ordinal, *including* names held by only one pope (`rp:francis-i`, `rp:lando-i`,
   `rp:linus-i`). Canonical IDs must be stable over time: if a future pope takes the
   name Francis, the label "Pope Francis" may become "Pope Francis I", but the
   identifier `rp:francis-i` never changes. Minting bare names and adding ordinals
   later would break stability; minting ordinals from day one costs nothing.
3. **The Peter exception.** `rp:peter` carries no ordinal and no honorific. Peter is
   never styled "Pope Peter" nor "Peter I" in any usage, ecclesial or common. The ID
   is stable regardless: if a future pope were ever to take the name Peter, he would
   be Peter II (`rp:peter-ii`), and `rp:peter` remains untouched.
4. **No honorific in the slug.** The registry's `rp:` prefix ("Roman Pontiffs" /
   *Romani Pontifices*) already scopes the namespace; repeating "pope-" inside every
   identifier would be redundant, and would force the awkward "pope-peter". The
   cdcf-uri-scheme's `pope-{name}-{roman}` form is carried as a cross-reference
   attribute instead (§6).
5. **Compound names hyphenate:** `rp:john-paul-i`, `rp:john-paul-ii`.
6. **Ordinals follow official numbering,** including historical skips caused by
   antipopes or numbering errors (e.g. there is no legitimate John XX; the sequence
   passes from `rp:john-xix` to `rp:john-xxi`). CRPDR records the numbering as the
   Church uses it; it does not repair history.

### 2.2 Grammar (ABNF, per RFC 5234)

```abnf
rp-id     = "rp:" pontiff-key
pontiff-key = "peter" / named-key
named-key = name HYPHEN roman
name      = name-seg *(HYPHEN name-seg)
name-seg  = 1*ALPHA
roman     = 1*(%x69 / %x76 / %x78 / %x6C / %x63 / %x64 / %x6D)
                                        ; i v x l c d m, lowercase
ALPHA     = %x61-7A                     ; a-z, lowercase only
HYPHEN    = %x2D
```

Parsing note: the final hyphen-separated segment of a `named-key` is always the
ordinal. No papal name's final name-segment consists solely of Roman-numeral
letters, so the split is unambiguous in practice; the ordinal-mandatory rule (§2.1.2)
guarantees it formally for all keys except the literal `peter`.

The `pontiff-key` production conforms to the `slug` production of the cdcf-uri-scheme
ABNF (`appendix-d-abnf.abnf`, v0.3.0): lowercase ASCII letters, digits, hyphens.

## 3. Entity model: person, not pontificate

One record per **person** who has held the papacy; a pontiff's reigns are an
attribute array, not separate identities. This follows the CECDR principle that
circumstance is an attribute, not identity.

The forcing case is Benedict IX, who reigned three separate times (1032–1044, 1045,
1047–1048) and occupies three rows of the Vatican table (nn. 145, 147, 150). He is
**one** identifier — `rp:benedict-ix` — with three entries in `pontificates`.

Consequently the registry holds 265 person records covering the table's 267
pontificates (267 rows − 2 duplicate Benedict IX rows; count to be verified
mechanically at seed time).

## 4. Data schema

`data/pontiffs.json` — an array of person records:

```jsonc
{
  "id": "rp:benedict-ix",
  "name": "Benedict",              // English regnal name, no ordinal
  "ordinal": 9,                    // integer; null for rp:peter
  "roman": "ix",                   // lowercase roman numeral; null for rp:peter
  "label_en": "Benedict IX",       // display label per the Vatican table
  "secular_name": "Teofilatto dei conti di Tuscolo",  // null when unknown
  "birthplace": "Rome",            // as given by the table; null when absent
  "century": 11,                   // century of (first) accession per the table
  "pontificates": [
    {
      "number": 145,               // succession number in the Vatican table
      "start_raw": "1032",         // verbatim source string, always kept
      "end_raw": "1044",
      "start": "1032",             // parsed ISO-ish value(s), only when unambiguous
      "end": "1044"
    },
    { "number": 147, "start_raw": "10.III.1045", "end_raw": "1.V.1045", ... },
    { "number": 150, "start_raw": "8.XI.1047", "end_raw": "17.VII.1048", ... }
  ],
  "cdcf_person": "cdcf:person/pope-benedict-ix"   // cross-reference, see §6
}
```

### 4.1 Date handling

The source table's dates are irregular and must never be silently normalized:

- **Uncertainty:** "64 or 67", "108 or 109" → keep the raw string; a parsed
  `alternates` array (e.g. `["0064", "0067"]`) may be added where useful.
- **Double dates:** modern entries give election and inauguration together
  ("13,19.III.2013") → parsed as `elected: "2013-03-13"`,
  `inaugurated: "2013-03-19"`, raw string retained.
- **Open reigns:** the reigning pope has `end_raw: null`.

Rule of thumb: `*_raw` fields are the source of truth and always verbatim; parsed
fields exist only where parsing is mechanical and unambiguous.

## 5. Repository layout and seed pipeline

Mirrors CECDR:

```
crpdr/
├── README.md                  # what/why, ID scheme summary, CETF attribution
├── LICENSE                    # Apache-2.0
├── data/
│   ├── pontiffs.json          # the seed registry (generated)
│   └── source/holy-father.html  # committed snapshot of the Vatican page, with
│                                # retrieval date noted (provenance; no live scraping)
├── docs/
│   └── schema-proposal.md     # the proposed schema + open questions for committee
└── scripts/
    └── generate_seed.py       # parses the snapshot → pontiffs.json
```

The generator parses the committed snapshot, not the live site, so seed generation
is reproducible and the source citable. Editorial decisions that cannot be derived
mechanically (e.g. the Anacletus/Cletus slug, §7) live in an explicit override table
inside the script, as in CRMEDR's `ID_CORRECTIONS` pattern.

All IDs are **drafts pending committee review**, stated prominently in the README.

## 6. Relation to the cdcf-uri-scheme

Xudong Wang's `cdcf-uri-scheme` (v0.3.0) already legislates for papal identifiers:

- §3.2 [REV-02] unifies papal slugs to `pope-{name}-{roman}` (English) across the
  `cdcf:magisterium/` and `cdcf:person/` domains.
- §3.6.1 mandates the ordinal suffix even for sole name-holders — the same
  forward-stability reasoning as §2.1.2 above, with `cdcf:person/pope-francis-i`
  as its worked example.
- The ABNF restricts slugs to lowercase ASCII.

CRPDR conforms to the spec's character set, English-name choice, and
ordinal-always rule. Each record carries the spec's form as a `cdcf_person`
cross-reference so the mapping is mechanical: `rp:leo-xiv` ↔
`cdcf:person/pope-leo-xiv`.

**One deliberate divergence:** §3.6.1's blanket MUST implies `pope-peter-i`, which
matches no ecclesial or common usage. CRPDR mints `rp:peter` (its `cdcf_person`
cross-reference provisionally `cdcf:person/pope-peter-i` until upstream rules).

**Upstream actions** (to be filed as issues on `xudonglab/cdcf-uri-scheme`):

1. Propose a Peter exception (or an explicit clarification) to §3.6.1.
2. Propose registering CRPDR as the authoritative registry backing papal slugs,
   so the spec's `pope-{name}-{roman}` values are drawn from a maintained list
   rather than coined ad hoc.

## 7. Open questions for the committee

Recorded in `docs/schema-proposal.md`:

1. **Antipopes.** Out of scope for v1 (the Vatican table lists only legitimate
   pontiffs, and antipope lists have no single authoritative source). A future
   discriminated segment (e.g. `rp:antipope-<name>-<roman>`) is sketched for the
   committee to accept or reject; numbering collisions with legitimate popes
   (Clement VII, Benedict XIII) make the discriminator mandatory.
2. **"Anacletus or Cletus"** (Vatican table row 3). Lean `rp:anacletus-i`, with
   `cletus` recorded as an alias attribute; committee to confirm.
3. **Date-uncertainty representation** — is the raw-plus-parsed model of §4.1
   sufficient, or is a structured uncertainty type (EDTF) warranted?
4. **The Peter divergence** from cdcf-uri-scheme §3.6.1, pending the upstream issue.

## 8. Out of scope

- Antipopes (v1; see §7.1).
- Biographical detail beyond the Vatican table's columns (no episcopal lineage,
  canonization status, feast days — those belong to other registries or attributes
  added later by the committee).
- Latin/Italian/other-language labels (attribute additions welcome later; the ID
  language question is settled as English).
- Any assertion about disputed historical questions (regnal date scholarship,
  legitimacy disputes); CRPDR transcribes the Holy See's own table.
