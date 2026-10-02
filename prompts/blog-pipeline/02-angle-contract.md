# 02 — Angle contract

Один угол. Без вопросов пользователю.

**Вход:** {{задача / source / map-derived packet}}  
**map-derived:** пропусти — contract уже есть.

Выведи angle contract:

```json
{
  "input_mode": "{{mode}}",
  "archetype": "practical_review|case_study|guide|comparison|tutorial",
  "reader_job": "зачем читателю",
  "thesis": "один тезис",
  "evidence": [
    {"id": "e1", "claim_support": "...", "ref": "url или path"}
  ],
  "max_evidence": 3,
  "exclude": ["full transcript", "product catalog", "другие углы"],
  "primary_goal": "...",
  "primary_cta": "kruzhok|personal_corp|mentoring|none",
  "cta_reason_if_none": ""
}
```

Правила: 1 thesis · ≤3 evidence · exclude непустой · остальное в backlog, не в packet.

**Выход в issue:** contract JSON.  
Нельзя восстановить thesis/evidence → `editorial_blocked`.
