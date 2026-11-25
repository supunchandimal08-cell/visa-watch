# Monitor Comparison Behaviour

**Review date:** 25 November 2026  
**Code:** `monitor.py`

## Confirmed default

In `load_sources()`, the monitor normalises each configured entry using:

```python
"compare_text": item.get("compare_text", True) is not False
```

Therefore:

- If `compare_text` is missing, text comparison is enabled.
- If `compare_text` is `true`, text comparison is enabled.
- If `compare_text` is `false`, only page availability is checked; page text is not compared.

The default is **ON**. This is a technical default, not a legal or quality approval of that source.

## Explicit result field improvement

The monitor now reports `content_compared` explicitly in its result items:

- `true`: the visible HTML text was read and fingerprinted.
- `false`: text comparison was disabled, the page could not be read, or the response was not an HTML page suitable for the current parser.

This makes the distinction visible to the dashboard and manual-review process. It does not mean that every legal detail on the page was semantically checked.

## Important technical limits

- A page-text hash can change because of navigation, formatting, cookie notices, timestamps or other non-policy content.
- A page can change in a legally important way without the extracted first 1 MB changing.
- PDF and non-HTML pages are not parsed by the current HTML text extractor.
- Availability-only sources must be manually opened and checked by a counsellor.
- A detected difference is a review candidate, never an automatically confirmed immigration-rule change.

## Counsellor rule

Always open the official source and check the exact visa category, applicant circumstances, publication date, commencement/effective date, exceptions and transitional rules. Record the human reviewer. If the source cannot be verified, mark the item **Needs review** and do not present it as confirmed advice.

## Related documents

- [Official Source Register](./OFFICIAL-SOURCE-REGISTER.md)
- [Source Inventory Data Quality Review](./SOURCE-INVENTORY-DATA-QUALITY-REVIEW.md)
- [Immigration Rule Verification Checklist](./IMMIGRATION-RULE-VERIFICATION-CHECKLIST.md)
