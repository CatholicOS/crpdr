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
   (`rp:francis-i`, `rp:lando-i`). In actual usage a regnal name carries no
   numeral until a later pope chooses the same name: Francis was never styled
   "Francis I" during his pontificate, just as Leo the Great was simply "Leo"
   until Leo II (682) retroactively made him "Leo I". A canonical identifier,
   however, must be stable, so it cannot migrate from a bare slug to a
   numbered one the day a namesake is elected — that shift belongs to
   *labels*, never to identifiers. This leaves exactly two stable
   conventions: mint the ordinal for every first-of-name from day one, or
   never mint it for a first-of-name at all. CRPDR settles on the first, for
   three reasons: (a) history has already decided the labels for reused
   names — 37 of the 82 regnal names have been borne by two or more popes
   (John by 21) — so bare first-of-name slugs would permanently diverge from
   universal usage for all of them (`rp:leo` for Leo the Great) and for any
   name reused in the future; (b) a mandatory ordinal gives the grammar its
   parsing property that the final hyphen-separated segment is always the
   ordinal; (c) it conforms to cdcf-uri-scheme §3.6.1, which mandates the
   ordinal "even for names held by only one pope, to guarantee forward
   stability". Labels remain free to track usage: `label_en` keeps the
   table's styling ("Francis"), and may one day become "Francis I" without
   `rp:francis-i` moving.
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
  "birth_country": null,           // ISO 3166-1 alpha-2 of the modern country
                                   // of the birthplace; null when the cell is
                                   // blank, names no mappable place, or the
                                   // modern attribution is contested
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

A record may additionally carry a `note` field flagging any enrichment beyond
the source table (see open question n. 5); records without a `note` are pure
transcriptions.

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

### Birth country

`birth_country` is the ISO 3166-1 alpha-2 code of the modern country of the
pope's place of birth, mapped **by the table's Birth string as printed**
(the generator's `BIRTH_COUNTRIES` table, whose completeness against the
source is enforced at generation time):

- Places and regions lying wholly within one modern country map to it —
  Rome, Tuscia, Sicily and Sardinia → `IT`; Aquitaine, the Limousin cluster
  and Savoy (Tarentaise) → `FR`; Saxony, Swabia and Bavaria → `DE`;
  Dalmatia → `HR`; Nicopolis (Epirus) → `GR`.
- The string is mapped as printed, not re-researched per person: "Syria"
  → `SY` even though the ancient province also covered Antioch (today in
  Türkiye).
- "Africa" (the Roman province) → `TN`, its Carthaginian heartland.
- Strings that name no mappable place ("Unknown"; Formosus's "Bishop of
  Portus", an office) and places whose modern attribution is contested
  (Bethsaida; Jerusalem, for which ISO 3166-1 assigns no covering code) map
  to `null`, with a per-record `note` where the reason is not self-evident.
- One per-record enrichment overrides the string mapping: Damasus II
  (table: "Tyrol") carries `birth_country: "DE"` — see open question n. 5.

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
5. **Enrichments beyond the table.** Applied through the generator's explicit
   `ENRICHMENTS` override and always flagged in the record's `note` field;
   records without a `note` are pure transcriptions. The seed carries three
   value enrichments and two explanatory notes:
   - `rp:peter.secular_name = "Simon"` (Mt 16:17; Jn 1:42). The source table
     leaves that cell blank — presumably because Peter's renaming was
     Christ's act, not a regnal-name choice at election — even though its own
     convention elsewhere fills the cell precisely when the pre-election name
     differs (first at John II, born Mercurio, 533; and notably John XIV and
     Sergius IV, both born Pietro, who changed their names out of reverence
     for the Apostle).
   - `rp:damasus-ii.birth_country = "DE"`: the table's "Tyrol" reflects his
     see of Brixen, but he was born Poppo at Pildenau in Bavaria — the Liber
     Pontificalis styles him "natione Noricus, qui alio vocabulo Bayuuarius
     dicitur".
   - `rp:callistus-i.birthplace = "Rome?"` with `birth_country = "IT"`: the
     table leaves the cell blank; Rome is a conjecture — marked "?" as
     presumption, not attestation — since his recorded life unfolds there,
     where he had been a slave before his ordination. The "?" convention is
     itself proposed here for any future conjectural value.
   - Notes without a value change on `rp:theodore-i` (Jerusalem: no covering
     ISO code) and `rp:formosus-i` ("Bishop of Portus" is an office, not a
     birthplace); `rp:peter`'s note also covers his null `birth_country`
     (Bethsaida's modern attribution is contested).
   Committee to confirm the enrichments and the mechanism.
6. **The `birth_country` mapping.** The string-level mapping policy above —
   in particular `TN` for the Roman province of Africa, `SY` for "Syria" as
   printed, and the null-with-note treatment of Bethsaida and Jerusalem — is
   an interpretive layer over the table. Committee to review the
   `BIRTH_COUNTRIES` table as a whole.
