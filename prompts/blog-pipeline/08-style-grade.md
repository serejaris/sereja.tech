# 08 — Style grade

**Вход:** {{draft path}}

```bash
python3 ~/.claude/skills/blog-post/grade.py {{draft.md}}
# practical_review:
# python3 ~/.claude/skills/blog-post/grade.py {{draft.md}} --max-words 1500
```

PASS только если: `STYLE=PASS` **и** score ≥ 8 **и** слова в коридоре.

FAIL → rewrite (тот же contract) → снова 08.  
Не идти дальше при FAIL.

**Выход:** verdict → issue.
