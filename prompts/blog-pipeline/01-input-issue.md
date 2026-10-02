# 01 — Input + Issue

Определи input mode и создай tracking issue. Не спрашивай пользователя.

**Вход:** {{задача / source paths}}

**Mode:**
- topic card / packet готов → `map-derived` (дальше с 03)
- стрим / транскрипт → стоп, skill `stream-to-post`
- урок → `lesson-derived`
- тема без стрима → `task`
- иначе → `other`

**Сделай:**
1. mode + owner goals (из задачи / author-bible / HQ)
2. source refs (пути/id only)
3. issue в `serejaris/sereja.tech`, label `blog`

```bash
gh issue create -R serejaris/sereja.tech \
  --title "blog: {{тема кратко}}" \
  --label blog \
  --body "Тема: {{тема}}
Input mode: {{mode}}
Archetype: pending
Дата: $(date +%Y-%m-%d)
Статус: Phase 0 — Input
editorial_rewrite_count: 0"
```

**Выход в issue:** mode, goals, issue number.  
Нет фактов под тезис → `editorial_blocked`.
