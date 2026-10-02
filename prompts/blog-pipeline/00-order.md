# Blog pipeline — порядок

Копируй файлы по номеру. Вставляй артефакт прошлой фазы вместо `{{...}}`.

| # | Файл | Выход |
|---|------|--------|
| 01 | input-issue | issue + mode |
| 02 | angle-contract | contract JSON |
| 03 | research | compact facts |
| 04 | related-posts | related JSON |
| 05 | writer-packet | packet |
| 06 | write-draft | draft.md |
| 07 | deaify | clean draft |
| 08 | style-grade | STYLE=PASS |
| 09 | fact-gate | PASS/FAIL |
| 10 | voice-gate | PASS/FAIL |
| 11 | reverse-outline | outline |
| 12 | editorial-gate | ready / blocked |
| 13 | title-cta | title + cta |
| 14 | editorial-lint | exit 0 |
| 15 | deploy-telegram | URL |

Стрим → сначала `stream-to-post`, потом с 03 (mode: map-derived).  
FAIL ×3 → `editorial_blocked`, шаги 13–15 не делать.
