---
title: "MIDI + OBS + Claude Code: от идеи до работающего решения за 3 часа"
date: 2026-01-11
description: "Как я настроил MIDI-контроллер для переключения сцен в OBS и написал LED-индикатор с помощью Claude Code. Полный разбор: velocity, SysEx, EventClient."
tags: ["midi", "obs", "claude code"]
section: Вайбкодинг
---

У меня лежал Arturia MiniLab 3. Использовал только для музыки.

Подумал — почему бы не переключать им сцены в OBS во время стримов?

Три часа с Claude Code. Результат: пэды переключают сцены, активная сцена подсвечивается.

## Задача

Хотел простую вещь: нажимаю Pad 1 — включается сцена "Десктоп". Pad 2 — камера. Pad 3 — телефон. Без мыши, без горячих клавиш.

Бонус: чтобы пэд активной сцены светился зелёным. Раньше переключался мышкой во время стрима — терял фокус, пару раз нажимал не туда. С пэдами переключаюсь вслепую.

## Хронология

**0:00** — Описал задачу Claude Code. Он провёл исследование через Exa, нашёл obs-midi-mg как лучший вариант для macOS.

**0:15** — Плагин установлен. Устройство видит. Создал биндинг через UI — не работает.

**0:30** — Claude Code предложил поставить MIDI Monitor. Оказалось — пэды отправляют разную velocity при каждом ударе.

**0:45** — Нашли решение: velocity ignore mode. Дважды кликнуть на "Velocity" в настройках биндинга. Заработало.

**1:00** — Попросил добавить третий пэд программно. Claude Code прочитал JSON-конфиг, добавил биндинг, перезапустил OBS.

**1:30** — Захотел LED-индикатор. Claude Code нашёл SysEx-коды для MiniLab 3, написал Python-скрипт.

**2:00** — Светятся не пэды, а кнопки Shift/Hold. Оказалось — пэды начинаются с индекса 4, не 0. Исправили.

**2:30** — Индикатор работает, но иногда пропускает. Переписали с polling на EventClient. Мгновенная реакция.

**3:00** — Не получает события. Оказалось — в obsws-python callback должен называться on_current_program_scene_changed. Исправили. Работает.

## Главные грабли

### 1. Velocity

Пэды MiniLab чувствительны к силе удара. Каждое нажатие — разное значение: 21, 45, 67. Плагин записывает конкретное значение при настройке. Ударил чуть сильнее — биндинг молчит.

{{< callout warning "Решение" >}}
Дважды кликнуть на "Velocity" в настройках биндинга. Значение станет прочерком — плагин будет игнорировать velocity.
{{< /callout >}}

В JSON это выглядит так:

```json
"velocity": {"state": 2, "index": 0, "min": 0, "max": 127}
```

`state: 2` — игнорировать. `state: 0` — фиксированное значение.

### 2. LED индексы MiniLab 3

Отправил цвет на индекс 0 — загорелась кнопка Shift. Индекс 1 — Oct-. Индекс 2 — Hold.

Пэды начинаются с индекса 4:

| Элемент | LED Index |
|---------|-----------|
| Shift | 0 |
| Oct - | 1 |
| Hold | 2 |
| Oct + | 3 |
| Pad 1 | 4 |
| Pad 2 | 5 |
| Pad 3 | 6 |
| ... | ... |

### 3. obsws-python callback naming

Написал функцию `_on_scene_change`. EventClient её игнорирует. Никаких ошибок, просто молчит.

{{< callout insight >}}
Имя callback функции = `on_` + snake_case имя события. Для CurrentProgramSceneChanged нужно `on_current_program_scene_changed`.
{{< /callout >}}

## Роль Claude Code

Я не писал ни строчки кода. Вот что делал Claude Code:

- **Исследование** — нашёл obs-midi-mg через Exa, сравнил с альтернативами
- **Установка** прошла быстро: pkg, установщик, готово
- С **диагностикой** повозились: MIDI Monitor показал проблему с velocity
- **Конфигурация** — JSON напрямую, без UI
- Python-скрипт для **LED индикатора** — с нуля
- **Отладка**: индексы пэдов оказались не 0-7, а 4-11
- Всё **задокументировал** в правила для следующих сессий

Это и есть вайбкодинг: описываешь что хочешь, агент делает.

## Итоговый стек

| Компонент | Назначение |
|-----------|------------|
| obs-midi-mg | Переключение сцен по MIDI |
| scene_indicator.py | LED индикатор активной сцены |
| obsws-python | WebSocket события от OBS |
| mido + python-rtmidi | Отправка SysEx на MiniLab |

## Код индикатора

Ключевые части:

```python
def set_pad_color(led_index, r, g, b):
    # F0 00 20 6B 7F 42 02 02 16 [led] [r] [g] [b] F7
    data = [0x00, 0x20, 0x6B, 0x7F, 0x42,
            0x02, 0x02, 0x16, led_index, r, g, b]
    port.send(mido.Message('sysex', data=data))
```

```python
# Имя функции ДОЛЖНО соответствовать событию
def on_current_program_scene_changed(self, data):
    scene_name = data.scene_name
    self._update_pads(scene_name)
```

## Запуск

```bash
# Установка
cd ~/Documents/GitHub/obs-midi
uv venv && uv pip install -r requirements.txt

# Тесты
source .venv/bin/activate
python scene_indicator.py --test

# Запуск
python scene_indicator.py
```

Не забудь включить OBS WebSocket: Tools → WebSocket Server Settings → Enable.

## Выводы

Три часа — от "хочу переключать сцены пэдами" до работающего решения с LED-индикатором. Без написания кода вручную.

Claude Code не просто генерирует код — он ставит MIDI Monitor, читает логи, правит конфиг. Я описывал проблему ("не работает"), он находил причину и исправлял.

## Источники

- [obs-midi-mg на GitHub](https://github.com/nhielost/obs-midi-mg)
- [obsws-python — WebSocket клиент](https://github.com/aatikturk/obsws-python)
- [MiniLab 3 SysEx коды](https://gist.github.com/Janiczek/04a87c2534b9d1435a1d8159c742d260)
- [Axios: Claude Code и вайбкодинг](https://www.axios.com/2026/01/07/anthropics-claude-code-vibe-coding)
- [The Vibe Coding Stack for 2026](https://craftbettersoftware.com/p/the-vibe-coding-stack-for-2026)
