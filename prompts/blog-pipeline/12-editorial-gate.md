# 12 — Editorial gate

Не «хорошая ли статья». Допустимость по контракту.

**Входы:** draft + reverse outline + contract

FAIL если есть:
- genre_collision · thesis_drift · transcript_chronology
- removable_section · missing_early_verdict
- too_many_cases · too_many_raw_quotes
- product_catalog · cta_competition
- title_intro_conclusion_mismatch · stream_narration

**Выход:**
```
ready_for_autonomous_publish
# или
FAIL: [codes]
editorial_rewrite_count: {{n}}
```

FAIL + n < 3 → rewrite 06–12, тот же contract.  
FAIL + n ≥ 3 → `editorial_blocked` (стоп, без 13–15).  
PASS ≠ «отличная статья».
