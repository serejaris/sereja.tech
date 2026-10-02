# 09 — Fact gate

Независимый судья (не автор draft).

**Входы:** draft + packet + sources

Проверь:
- каждый checkable claim ∈ packet / verified facts / author-bible
- нет выдуманных метрик, дат, «в лайве делал X» без ref
- map-derived: сверка с topic card, не с транскриптом

**Выход:**
```
FACT: PASS|FAIL
findings:
  - ...
```

FAIL → rewrite ≤3 или `editorial_blocked` если source не чинится.
