# 15 — Deploy + Telegram

Только если 08–12–14 все PASS.

1. OG: corp-media → `static/images/blog/{{slug}}-preview.png`
2. Файл: `content/blog/{{slug}}.md`
3. Commit + push (Git → Vercel, не local vercel deploy)

```bash
git add content/blog/{{slug}}.md static/images/blog/{{slug}}-preview.png
git commit -m "feat(blog): add {{title}}"
git push
```

4. Telegram queue (blog-to-telegram) после publish  
5. README «Последние статьи» — новая первой  
6. `gh issue close`

Любой FAIL ранее → этот файл не запускать.
