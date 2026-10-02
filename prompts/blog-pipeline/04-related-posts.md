# 04 — Related posts

**Вход:** tags / thesis: {{tags или thesis}}

```bash
python3 ~/.claude/skills/blog-post/find_related_posts.py "{{tag1,tag2,tag3}}"
```

Выбери 3–5 релевантных постов (или `[]`).

**Выход:**
```json
[
  {"slug": "...", "title": "...", "link_text": "..."}
]
```

Только короткий JSON → в issue и в packet. Не дамп всего блога.
