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
