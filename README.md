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
  regnal name and ordinal, aliases, secular name, birthplace with the ISO
  3166-1 alpha-2 code of its modern country, dated pontificates (source
  strings verbatim plus parsed dates where unambiguous), and its
  `cdcf:person/` cross-reference.
- [`registry/pontiffs.md`](registry/pontiffs.md) — the same registry as a
  human-readable table, one row per pontificate in succession order.
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

### Where the Holy See's list comes from

The vatican.va table corresponds to the list of Roman Pontiffs that the Holy
See publishes each year in the **Annuario Pontificio**, its official yearbook,
compiled by the Central Office of Church Statistics of the Secretariat of
State. The modern form of that list goes back to a critical revision by
**Angelo Mercati**, prefect of the Vatican Secret Archive, adopted in the 1947
edition. The Annuario itself cautions that for some periods — the earliest
centuries, and contested elections such as those of the mid-11th century — the
dates and even the legitimacy of particular pontificates cannot be established
with certainty; CRPDR inherits those uncertainties rather than resolving them.

Behind the Annuario stands a long tradition of historical sources. They are
not used to generate the registry, but they are what our knowledge of the
popes ultimately rests on, and they are the natural references for the
committee when a record needs scrutiny:

- **Early succession lists (2nd–4th centuries).** Irenaeus of Lyons,
  *Adversus haereses* III.3.3 (c. 180), gives the Roman succession from Linus
  to Eleutherius, a list already circulating in Rome; Hegesippus (preserved in
  Eusebius) compiled a similar one. Eusebius of Caesarea's *Ecclesiastical
  History* and *Chronicle* (early 4th century) add reign lengths. The
  **Liberian Catalogue**, part of the Chronography of 354, runs to Pope
  Liberius with dates and consular years, and was a direct source for the
  Liber Pontificalis. Later lists appear in Optatus of Milevis and Augustine
  (Ep. 53).
- **The [Liber Pontificalis](https://en.wikipedia.org/wiki/Liber_Pontificalis).**
  A collection of papal biographies first compiled in Rome in the 6th century
  and continued, entry by entry, into the late 9th century, with medieval
  continuations reaching the 15th. Each life typically records origin
  (*natione …*), father's name, length of reign, ordinations, buildings and
  donations, and burial place. Its early entries are largely legendary or
  reconstructed; from about the 6th century it becomes a near-contemporary
  record kept in the papal administration. The standard critical edition is
  Louis Duchesne's (*Le Liber Pontificalis*, 1886–1892; supplementary volume
  by Cyrille Vogel, 1957); Theodor Mommsen edited the text to 715 for the
  *Monumenta Germaniae Historica* (1898). CRPDR already cites it where it
  documents a birthplace more precisely than the table (see the
  attested-birthplace notes in [docs/schema-proposal.md](docs/schema-proposal.md)).
- **Papal registers.** The *Regesta Pontificum Romanorum* calendar the
  surviving papal letters and acts — Philipp Jaffé's to 1198 (2nd ed.
  1885–1888) and August Potthast's for 1198–1304 — and are a principal tool
  for dating medieval pontificates. The Vatican Apostolic Archive preserves the
  registers themselves: a continuous series from Innocent III (1198) onward,
  with earlier survivals such as the register of Gregory VII.
- **Official acts (modern pontificates).** Elections, deaths, and
  renunciations are recorded in the *Acta Sanctae Sedis* (1865–1908) and its
  successor, the *Acta Apostolicae Sedis* (1909–), the Holy See's official
  gazette.

## License

The data and documentation in this repository are licensed under the [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License](https://creativecommons.org/licenses/by-nc-nd/4.0/) (CC BY-NC-ND 4.0). See [`LICENSE`](LICENSE) for the full legal code.

The source code in [`scripts/`](scripts/) is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). See [`scripts/LICENSE`](scripts/LICENSE).

The source snapshot [`data/source/holy-father-table.html`](data/source/holy-father-table.html) is an excerpt of the Holy See's website ([vatican.va](https://www.vatican.va/content/vatican/en/holy-father.html)), retained for provenance and reproducible generation. It is not covered by either license above; its reuse is governed by the [Vatican Legal Notes](https://www.vatican.va/content/vatican/en/legal-notes.html).
