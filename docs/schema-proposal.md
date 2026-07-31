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
    { "number": 145, "start_raw": "...VIII or IX.1032",
      "end_raw": "...IX.1044", "end": "1044-09" },
    { "number": 147, "start_raw": "10.III.1045", "end_raw": "1.V.1045",
      "start": "1045-03-10", "end": "1045-05-01" },
    { "number": 150, "start_raw": "...X.1047", "end_raw": "... VIII.1048",
      "start": "1047-10", "end": "1048-08" }
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
  (`...VIII.827` → `0827-08`), year partials (`... 236` → `0236`), and — in
  the beginning column only — the election/inauguration double dates
  (`13,19.III.2013` → `start_elected: 2013-03-13`,
  `start_inaugurated: 2013-03-19`).
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
   ([EDTF](https://www.loc.gov/standards/datetime/)) warranted for the 49
   irregular strings currently kept raw-only?
4. **The Peter divergence** from cdcf-uri-scheme §3.6.1, pending
   [xudonglab/cdcf-uri-scheme#3](https://github.com/xudonglab/cdcf-uri-scheme/issues/3)
   (the proposed Peter exception; see also
   [#4](https://github.com/xudonglab/cdcf-uri-scheme/issues/4), which proposes
   CRPDR as the maintained registry behind the spec's papal slugs).
