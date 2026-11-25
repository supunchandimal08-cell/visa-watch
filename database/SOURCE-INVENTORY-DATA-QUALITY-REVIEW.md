# Official Source Inventory — Data Quality Review

**Review date:** 25 November 2026  
**File reviewed:** `data/sources.json`  
**Status:** Audit notes only; no immigration rule has been approved by this review.

## Snapshot

The inventory contains **99 source entries** across **18 country / jurisdiction labels**.

| Field | Entries containing field | Entries missing field |
|---|---:|---:|
| `country` | 99 | 0 |
| `name` | 99 | 0 |
| `url` | 99 | 0 |
| `compare_text` | 86 | 13 |
| `note` | 90 | 9 |
| `authority` | 1 | 98 |
| `jurisdiction` | 1 | 98 |
| `category` | 1 | 98 |

The 13 entries without an explicit `compare_text` value may use the monitor's default behaviour. Confirm the implementation in `monitor.py` before interpreting those entries as text-comparison or availability-only checks.

## Entries by country / jurisdiction label

| Label | Entries |
|---|---:|
| UK | 7 |
| Canada | 8 |
| Australia | 7 |
| New Zealand | 9 |
| USA | 4 |
| UAE / Dubai | 12 |
| Europe / Schengen | 2 |
| Germany | 4 |
| UAE | 2 |
| Ireland | 8 |
| France | 5 |
| Netherlands | 7 |
| Italy | 4 |
| Finland | 6 |
| Sweden | 4 |
| Iceland | 5 |
| Japan | 3 |
| Spain | 2 |

## Findings and safe next actions

1. **Authority metadata is incomplete.** Only one record currently contains all of `authority`, `jurisdiction` and `category`. Do not infer these values automatically from a URL or country label. Populate them only after a human verifies the issuing authority and scope.
2. **Country labels need a controlled vocabulary.** The inventory has both `UAE` and `UAE / Dubai`. Keep them distinct only where the source genuinely has federal versus Dubai-specific jurisdiction. Do not merge without checking the source's legal scope.
3. **Europe is not one student-visa jurisdiction.** The country-specific authorities must remain separately identified. EU-level pages provide context and do not replace national immigration rules.
4. **Monitoring mode needs to be explicit.** Check the monitor code's default when `compare_text` is omitted. Set an explicit boolean only after deciding whether text comparison is technically appropriate for that page.
5. **Notes are not a substitute for evidence.** Every client-facing rule derived from a source still needs a direct official URL, access date, publication date where available, effective date where applicable, and named human reviewer.
6. **Do not bulk-edit source metadata yet.** A wrong authority, jurisdiction or category could cause a counsellor to apply a rule to the wrong applicant. Use a staged, reviewed update.

## Recommended next data-cleanup sequence

- Confirm the monitor's default behaviour for `compare_text`.
- Review each source URL and identify its actual issuing authority.
- Assign a controlled jurisdiction label (federal, national, province/state, emirate, EU-level or consular post).
- Assign a narrow category such as student entry, residence, work rights, funds, provider eligibility, post-study route or application process.
- Record last human verification date and reviewer in a future structured schema.
- Run automated JSON validation and a manual sample review before merging metadata changes.

## Important warning

This report checks the shape and counts of the JSON inventory only. It does **not** verify that all 99 URLs are reachable, current, legally authoritative or correct for a particular applicant. Automated monitoring is change detection, not legal interpretation. Do not use this report alone to advise a client.
