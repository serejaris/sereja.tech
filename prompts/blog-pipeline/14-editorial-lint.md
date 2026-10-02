# 14 — editorial_gate.py

Машинный structural lint. Не оценка качества.

**Вход:** {{draft.md}} · archetype · evidence ids

```bash
python3 ~/.claude/skills/blog-post/editorial_gate.py {{draft.md}} \
  --archetype {{archetype}} \
  --evidence-ids {{e1,e2,e3}}
# map-derived обязательно:
#   --max-stream-narration 2
```

Exit 0 → PASS.  
Exit 1 → FAIL → rewrite / blocked.  
Не публиковать при FAIL.

**Выход:** stdout/JSON → issue.
