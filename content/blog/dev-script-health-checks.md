---
title: "Один скрипт вместо трёх терминалов"
date: 2026-01-18
description: "Как настроить dev.sh с health checks для автоматического запуска backend и frontend"
tags: ["claude code", "devops"]
knowledge:
  problem: "Ежедневный ручной запуск backend и frontend занимает 5 минут и путает AI-агентов, которые дебажат несуществующие баги"
  solution: "Единый dev.sh с health checks через curl, автоочисткой портов и документацией в CLAUDE.md"
  pattern: "dev-script-health-checks"
  tools: ["Bash", "FastAPI", "React", "curl"]
  takeaways:
    - "Время запуска dev-окружения сократилось с 5 минут до 30 секунд"
    - "Health check через curl -f предотвращает запуск фронтенда до готовности бэкенда"
    - "Агент потратил 15 минут на дебаг 404, хотя бэкенд просто не был запущен"
    - "Документация в CLAUDE.md не даёт агенту запускать сервисы по отдельности"
  metrics:
    startup_before_seconds: 300
    startup_after_seconds: 30
---

Открыл проект, запустил фронтенд — ошибки 404 в консоли. Бэкенд не работает: на порту 8000 висит процесс от вчерашней сессии.

Каждый раз.

## Проблема

У меня fullstack на FastAPI + React. Запуск выглядит так:

1. `lsof -ti :8000 | xargs kill` — освободить порт
2. Терминал №1: запустить бэкенд
3. Ждать, пока стартанёт
4. Терминал №2: фронтенд
5. Проверить, что оба отвечают

Пять шагов. По-моему, терял минут пять каждое утро.

Агенты спотыкаются ещё сильнее. Вчера Claude Code увидел 404 на `/api/students` и полез править роутер — хотя бэкенд просто не был запущен. Потратил 15 минут на отладку несуществующего бага.

## Решение

Попросил агента:

{{< callout type="insight" >}}
Сделай ./dev.sh — запускает backend и frontend, проверяет health endpoints, показывает статус. Посмотри лучшие практики через Exa.
{{< /callout >}}

Нашёл три паттерна:

- **Единая точка входа** — один `./dev.sh` вместо двух терминалов
- **Health checks** — `curl -f localhost:8000/health` перед стартом фронтенда
- **Автоочистка портов** — убить зомби-процессы перед запуском

Скрипт:

```bash
#!/bin/bash
wait_for_health() {
    local url=$1
    local name=$2
    echo -n "  $name"
    for i in $(seq 1 30); do
        curl -sf "$url" > /dev/null 2>&1 && echo " ✓" && return 0
        echo -n "."
        sleep 1
    done
    echo " ✗" && return 1
}

kill_port() {
    lsof -ti :$1 2>/dev/null | xargs kill -9 2>/dev/null || true
}

kill_port 8000
uvicorn app.main:app --reload --port 8000 &

wait_for_health "http://localhost:8000/health" "Backend"
wait_for_health "http://localhost:8000/api/students" "API"

npm run dev &
wait_for_health "http://localhost:5173" "Frontend"

echo "=== Ready ==="
wait
```

## Результат

Запуск — одна команда. Время старта: 30 секунд вместо пяти минут.

```
=== Mentor Platform ===

Health checks:
  Backend ✓
  API /api/students ✓
  Frontend ✓

=== Ready ===
```

Сломалось? Сразу видно где — красный крестик напротив упавшего сервиса.

## Документация для агента

В CLAUDE.md добавил:

```markdown
| ✅ Always | Use `./dev.sh` to start dev environment |
```

Теперь агент не лезет запускать бэкенд и фронтенд по отдельности.

## Источники

- [Monorepo best practices](https://graphite.dev/guides/monorepo-frontend-backend-best-practices) — Graphite
- [Validate scripts for monorepos](https://blog.devgenius.io/how-to-create-a-validate-script-for-formatting-linting-and-type-checking-in-a-monorepo-fb21172618d9) — Dev Genius
