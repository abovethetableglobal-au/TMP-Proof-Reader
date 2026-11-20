# Public test documents (not committed — fetch from source)

| ID | Document | Source URL | SHA-256 (first 16) | Fetched |
|---|---|---|---|---|
| PUB-01 | MRWA Works on Roads TMP template (April 2026 edition, 42 pp as PDF) | https://www.mainroads.wa.gov.au/globalassets/technical-commercial/working-on-roads/traffic-management/tmp-template.docx | f423db4aa7e17e6d | 2026-11-20 |

Recreate:
```bash
curl -sSL -o test-library/public/mrwa-tmp-template.docx "https://www.mainroads.wa.gov.au/globalassets/technical-commercial/working-on-roads/traffic-management/tmp-template.docx"
```
```bash
cd test-library/public && soffice --headless --convert-to pdf mrwa-tmp-template.docx
```
