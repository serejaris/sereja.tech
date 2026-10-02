# 13 — Title + CTA

Только после `ready_for_autonomous_publish`. Без approval пользователя.

**Вход:** contract + draft

**Title:** 5 candidates (≤60, конкретика, без AI-slop) → селектор выбирает 1.

**CTA** только из contract:
| primary_cta | frontmatter |
|-------------|-------------|
| kruzhok / personal_corp / mentoring | `cta` + `cta_code: blog_{{slug}}` + блок cta-block |
| none | `cta: none` + `cta_reason` |

description ≤160.

**Выход:** final title, description, cta fields → frontmatter + issue.
