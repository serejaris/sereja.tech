---
title: "MIDI-контроллер для OBS: переключаю сцены пэдами"
date: 2026-01-11
description: "Настроил Arturia MiniLab 3 для переключения сцен в OBS через obs-midi-mg. Главная проблема — velocity. Показываю JSON-конфиг и как автоматизировать."
tags: ["midi", "obs", "стриминг"]
section: Стриминг
knowledge:
  problem: "Ручное переключение сцен в OBS через мышку неудобно при стриминге."
  solution: "Настройка obs-midi-mg плагина для переключения сцен MIDI-пэдами с velocity ignore mode."
  pattern: "midi-obs-binding"
  tools: ["OBS", "obs-midi-mg", "Arturia MiniLab 3", "MIDI Monitor", "Claude Code"]
  takeaways:
    - "Velocity по умолчанию фиксированная — нужен Ignore (state: 2) двойным кликом"
    - "MiniLab 3 User mode (Shift + Pad 2) нужен для OBS, DAW mode отправляет другие сообщения"
    - "Channel 10 — стандарт для пэдов, Note 36 — первый пэд, каждый следующий +1"
    - "JSON-конфиг obs-midi-mg можно редактировать программно через Claude Code"
    - "obs-midi-mg v3.1.1 работает на Mac, Windows, Linux"
  related:
    - slug: "midi-obs-claude-code"
      relation: "полный разбор с LED-индикатором и SysEx-кодами"
---

У меня лежал Arturia MiniLab 3. Использовал для музыки.

Подумал — почему бы не переключать им сцены в OBS?

Два часа отладки. Проблема оказалась в одном параметре.

## Что нужно

Любой MIDI-контроллер с пэдами или кнопками. MiniLab 3 подошёл идеально — 8 пэдов, каждый на свою сцену.

Плагин [obs-midi-mg](https://github.com/nhielost/obs-midi-mg). Работает на Mac, Windows, Linux. Версия 3.1.1 — последняя на январь 2026.

```bash
curl -LO "https://github.com/nhielost/obs-midi-mg/releases/download/3.1.1/obs-midi-mg-3.1.1-macos-universal.pkg"
open obs-midi-mg-*.pkg
```

После установки: OBS → Tools → obs-midi-mg. Выбираешь устройство, жмёшь Connect.

## Проблема с velocity

Создал биндинг. Нажал Listen, ударил по пэду. Плагин записал параметры. Сохранил. Нажимаю пэд — ничего.

Открыл MIDI Monitor. Пэды отправляют Note On с разной velocity. Каждый удар — новое значение: 21, 8, 45, 67. Зависит от силы нажатия.

А плагин записал конкретное значение. Velocity 21 — только velocity 21 и сработает. Ударил чуть сильнее — уже 25, биндинг молчит.

{{< callout warning "Velocity по умолчанию фиксированная" >}}
obs-midi-mg записывает точное значение velocity при Listen. Пэды с чувствительностью к силе удара будут работать нестабильно.
{{< /callout >}}

## Решение: режим Ignore

Дважды кликаешь на слово «Velocity» в настройках биндинга. Значение меняется на прочерк. Теперь плагин игнорирует velocity — срабатывает при любом значении.

{{< callout insight >}}
В конфиге это выглядит как `"velocity": {"state": 2, ...}`. State 0 — фиксированное значение, state 2 — игнорировать.
{{< /callout >}}

## Конфиг программно

Настраивать через UI долго. Каждый пэд — отдельный биндинг. Можно редактировать JSON напрямую.

Конфиг лежит тут:

```
~/Library/Application Support/obs-studio/plugin_config/obs-midi-mg/obs-midi-mg-config.json
```

Сначала нужны UUID сцен:

```bash
cat ~/Library/Application\ Support/obs-studio/basic/scenes/*.json | \
python3 -c "import sys,json; d=json.load(sys.stdin); \
[print(f'{s[\"name\"]}: {s[\"uuid\"]}') for s in d.get('sources',[]) \
if s.get('versioned_id')=='scene']"
```

Структура биндинга:

```json
{
  "name": "Pad 1 → Desktop",
  "enabled": true,
  "type": 0,
  "messages": [{
    "device": "Minilab3 MIDI",
    "channel": {"state": 0, "value": 10},
    "note": {"state": 0, "value": 36},
    "velocity": {"state": 2, "index": 0, "min": 0, "max": 127}
  }],
  "actions": [{
    "id": 4353,
    "scene": {"state": 0, "value": "UUID-СЦЕНЫ"}
  }]
}
```

Channel 10 — стандарт для пэдов MiniLab. Note 36 — первый пэд. Каждый следующий +1.

## MiniLab 3: режимы

У MiniLab три режима работы. Переключение: Shift + пэд 1/2/3.

| Комбинация | Режим | Для чего |
|------------|-------|----------|
| Shift + Pad 1 | Arturia | Analog Lab |
| Shift + Pad 2 | User | OBS, кастомные маппинги |
| Shift + Pad 3 | DAW | Ableton, Logic |

Для OBS нужен User mode. В DAW mode пэды отправляют другие сообщения.

## Автоматизация через Claude Code

Добавлять сцены вручную — рутина. Попросил Claude Code сделать это за меня.

Агент читает конфиг, находит UUID новой сцены, добавляет биндинг с правильными параметрами. Одна команда — готово.

```
claude: "добавь pad 3 на сцену iphone"
→ читает scenes/*.json, находит UUID
→ добавляет биндинг в конфиг
→ перезапусти OBS
```

Документацию по формату сохранил в `~/.claude/rules/obs-midi.md`. Теперь агент знает структуру и может редактировать конфиг.

## Итого

Работает. Pad 1 — десктоп. Pad 2 — камера. Pad 3 — телефон. Переключаюсь без мыши.

Главные грабли:
- Velocity — включить Ignore (state: 2)
- MiniLab — User mode (Shift + Pad 2)
- После правки JSON — перезапустить OBS

## Источники

- [obs-midi-mg на GitHub](https://github.com/nhielost/obs-midi-mg)
- [obs-midi-mg на OBS Forum](https://obsproject.com/forum/resources/obs-midi-mg.1570/)
- [Документация плагина](https://github.com/nhielost/obs-midi-mg/blob/master/docs/operations.md)
- [MIDI Monitor для macOS](https://www.snoize.com/MIDIMonitor/)
