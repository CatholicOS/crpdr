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
