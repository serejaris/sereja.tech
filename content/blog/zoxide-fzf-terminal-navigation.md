---
title: "zoxide + fzf: как перестать печатать пути в терминале"
date: 2026-01-15
description: "Практический гайд по настройке zoxide и fzf для быстрой навигации в терминале. Типичные ошибки, интерактивный выбор директорий, frecency-алгоритм."
tags: ["zoxide", "fzf", "терминал"]
section: Терминал
knowledge:
  problem: "Навигация по глубоким путям в терминале требует печати длинных путей каждый раз"
  solution: "zoxide запоминает посещённые директории и прыгает по ключевому слову, fzf добавляет интерактивный выбор"
  pattern: "frecency-navigation"
  tools: ["zoxide", "fzf", "Homebrew", "zsh"]
  takeaways:
    - "zoxide на Rust стартует за 5ms — в 10 раз быстрее autojump (50ms)"
    - "Алгоритм frecency комбинирует частоту и свежесть посещений директорий"
    - "alias z='cd' ломает zoxide — нужно использовать --cmd cd при инициализации"
    - "Пробел перед TAB переключает режим: z foo<TAB> — локальные директории, z foo <TAB> — база zoxide"
    - "За месяц в базе накапливается ~120 путей"
  metrics:
    startup_time_ms: 5
    autojump_startup_ms: 50
    speedup_factor: 10
    paths_per_month: 120
---

Установил zoxide. Не работает.

Полчаса искал причину — оказалось, сам сломал одной строкой.

Починил, добавил fzf. Теперь `z hsl` вместо `cd ~/Documents/GitHub/hsl-dashboard`.

## Что такое zoxide

Умный `cd`. Запоминает куда ты ходишь и потом прыгает туда по ключевому слову.

Написан на Rust, работает быстрее autojump в 10 раз. Стартует за 5ms против 50ms у autojump. На практике разница незаметна, но приятно.

Алгоритм называется frecency — комбинация частоты и свежести. Директория куда ходил вчера весит больше, чем та куда заглядывал месяц назад. Со временем старые пути опускаются вниз рейтинга.

## Установка

```bash
brew install zoxide
```

Потом добавить в `~/.zshrc`:

```bash
eval "$(zoxide init zsh)"
```

Перезапустить терминал. Всё.

## Как я сломал zoxide одной строкой

У меня в конфиге было:

```bash
eval "$(zoxide init zsh)"
alias z='cd'
```

Видишь проблему? Alias перезаписывает функцию `z`, которую создаёт zoxide. Вместо умного прыгуна получаем обычный cd.

Хуже того — ломается hook. zoxide записывает пути в базу через функцию `__zoxide_hook`, которая вызывается при каждой смене директории. Alias убивает эту связь.

{{< callout warning "Не перезаписывай z" >}}
Если хочешь заменить cd на zoxide целиком — используй `--cmd cd` при инициализации, а не alias.
{{< /callout >}}

Удалил строку с alias. Заработало.

## Как пользоваться

Сначала база пустая. Ходишь по директориям через cd — zoxide запоминает каждый переход.

```bash
cd ~/Documents/GitHub/my-project
cd ~/Downloads
cd /etc/nginx
```

Дня за два-три база заполнится. Дальше прыгаешь:

```bash
z my-project    # → ~/Documents/GitHub/my-project
z down          # → ~/Downloads
z nginx         # → /etc/nginx
```

Можно комбинировать слова: `z git my` найдёт что-то типа `~/Documents/GitHub/my-project`.

## Добавляем fzf для интерактивного выбора

Tab-completion для zoxide требует fzf. Без него `z foo<TAB>` работает только для локальных директорий.

```bash
brew install fzf
```

После этого открываются два режима:

| Ввод | Что делает |
|------|------------|
| `z foo<TAB>` | Completion локальных директорий |
| `z foo <TAB>` | Интерактивный выбор из базы zoxide |
| `zi foo` | То же самое — fzf-выбор |

Обрати внимание на пробел. `z foo<TAB>` и `z foo <TAB>` — разные вещи. С пробелом открывается fzf со списком всех путей из базы.

{{< callout insight >}}
Если не хочешь помнить про пробел — используй `zi`. Это alias для интерактивного режима. `zi git` сразу откроет fzf с фильтром.
{{< /callout >}}

## Полезные команды

| Команда | Что делает |
|---------|------------|
| `zoxide query -ls` | Показать всю базу с весами |
| `zoxide add /path` | Добавить путь вручную |
| `zoxide remove /path` | Удалить путь из базы |

## Альтернативы

Есть autojump, оригинальный z, fasd. Я выбрал zoxide.

Rust. Быстрее autojump в 10 раз — 5ms на старт против 50ms. На практике не замечаешь, но на слабых машинах разница есть.

fzf-интеграция из коробки. 32K звёзд на GitHub, активная разработка.

autojump работает, но медленнее. Оригинальный z — shell-скрипт, fuzzy search нет. fasd заархивирован в 2022.

## Итого

Две команды:

```bash
brew install zoxide fzf
echo 'eval "$(zoxide init zsh)"' >> ~/.zshrc
```

У меня в базе 120 путей за месяц. Чаще всего: `z hsl`, `z whisper`, `z claude`. Секунды на каждом переходе — за день набегает.

## Источники

- [zoxide на GitHub](https://github.com/ajeetdsouza/zoxide)
- [Официальный блог zoxide](https://zoxide.org/blog/)
- [zoxide vs autojump — сравнение производительности](https://zoxide.org/blog/zoxide-vs-autojump/)
- [zoxide: tips and tricks — Bozhidar Batsov](https://batsov.com/articles/2025/06/12/zoxide-tips-and-tricks/)
- [fzf на GitHub](https://github.com/junegunn/fzf)
