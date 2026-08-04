---
title: "Как подключить подписку Anthropic к Hermes"
date: 2026-08-04
description: "Проверенный путь: Hermes остаётся Telegram runtime, а Opus вызывается через официальный Claude Code CLI и подписку Anthropic без Extra Usage."
tags: ["hermes", "anthropic", "claude-code", "telegram", "вайбкодинг"]
image: "/images/blog/claude-max-hermes-telegram-preview.png"
cta: personal_corp
cta_code: pc_blog
---

Я хотел оставить Hermes самим ботом и подключить к нему Opus через действующую подписку Anthropic. Без API key, отдельного pay-as-you-go и Extra Usage.

Связка заработала. Hermes отвечает в Telegram-личке и topics, хранит свои сессии и память, вызывает свои tools.

Каждый основной model turn идёт через официальный Claude Code CLI.

Мой живой тест выполнен на Claude Max и Opus.

Архитектура привязана к авторизованной подписочной сессии Claude Code.

Max здесь пример проверенного тарифа. Сама схема опирается на подписочную сессию Claude Code.

## Как связаны Hermes, provider и Claude CLI

Здесь четыре слоя:

| Слой | Роль |
|---|---|
| Telegram | Доставляет сообщения существующему боту |
| Hermes | Ведёт gateway, сессии, память и tool loop |
| User provider | Переводит запрос Hermes в локальный вызов CLI |
| Claude Code CLI | Запускает Opus через подписочную сессию Anthropic |

User provider — это community-плагин для штатного каталога Hermes. Он поднимает OpenAI-compatible shim на 127.0.0.1:8765.

Hermes обращается к shim как к обычному model provider. Shim запускает официальный claude -p --model opus. Авторизацию и расход лимита контролирует Claude Code.

~~~text
Telegram
   ↕
Hermes gateway · sessions · memory · tools
   ↕
claude-code-cli provider на 127.0.0.1
   ↕
официальный claude -p --model opus
   ↕
подписка Anthropic
~~~

Официальный Telegram Channel Anthropic в этой схеме не участвует. Это был мой первый обход.

В нём Hermes полностью заменялся, поэтому исходная задача оставалась нерешённой.

## Почему здесь работает подписка

Native Anthropic OAuth в Hermes использует пул Extra Usage. При выключенном Extra Usage мой живой запрос завершался ошибкой out of extra usage.

Provider идёт другим путём. Он запускает официальный Claude Code CLI, уже авторизованный через аккаунт Claude.

Hermes не хранит Anthropic API key и не вызывает metered API напрямую.

В проверочном запуске Claude сообщил:

- authMethod=claude.ai;
- apiProvider=firstParty;
- apiKeySource=none;
- модель claude-opus-5;
- окно подписки five_hour разрешено;
- isUsingOverage=false;
- overage выключен на уровне организации.

Так я отделяю подписочный маршрут от случайного расхода API или Extra Usage.

## Какой код я использовал

Основа — community provider Ouroborosrex/hermes-claude-code-cli-provider.

Я зафиксировал base commit:

~~~text
09a3aec0ab7406c6a0731f858f1b4b7a99f0cb77
~~~

Из PR #12 взял два независимых исправления:

~~~text
8e5c74c2eb3017fd47f5d1d504625d3c87058b40
62420fb094a1124292bd4931781b45a8e7ab9633
~~~

Первое превращает ошибки CLI в HTTP-коды, понятные fallback-механизму Hermes.

Второе проверяет реально обслужившую модель и ловит тихую подмену Opus.

Мой hardening patch добавляет ещё три вещи:

- allowlist окружения дочернего claude;
- корректный context accounting для Hermes;
- совместимость с ProviderProfile в Hermes v0.14.

Allowlist важен. Процесс Hermes видит Telegram token и ключи других провайдеров. Передавать всё окружение в Claude CLI нельзя.

Patch оставляет системные переменные и OAuth-настройки Claude Code.

Anthropic API keys, cloud routing, Telegram token и ключи других провайдеров в subprocess не попадают.

Context patch тоже нужен. Внутренний system prompt Claude Code большой.

Если вернуть его usage в Hermes как пользовательский prompt, Hermes может слишком рано сжать контекст.

## Установка

Сначала сохраните container или VM, ~/.hermes, Telegram-конфиг и текущий provider. Зафиксируйте rollback-команды.

У одного Telegram bot token должен быть один poller. Старый gateway останавливайте только перед финальным переключением.

### 1. Установить Claude Code и войти в подписку

Установите официальный Claude Code CLI по документации Anthropic. На целевом сервере выполните:

~~~bash
claude auth login
claude auth status --json
~~~

Ожидаемый статус: вход через claude.ai, first-party provider и ваш subscription type.

Файл credentials держите с mode 0600. Не печатайте OAuth token в логи и не вставляйте его в конфиг Hermes.

### 2. Установить provider

~~~bash
export HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
plugin_dir="$HERMES_HOME/plugins/model-providers/claude-code-cli"

git clone https://github.com/Ouroborosrex/hermes-claude-code-cli-provider "$plugin_dir"
git -C "$plugin_dir" checkout 09a3aec0ab7406c6a0731f858f1b4b7a99f0cb77
git -C "$plugin_dir" fetch origin pull/12/head:pr-12
git -C "$plugin_dir" cherry-pick 8e5c74c2eb3017fd47f5d1d504625d3c87058b40
git -C "$plugin_dir" cherry-pick 62420fb094a1124292bd4931781b45a8e7ab9633
~~~

Скачайте мой versioned patch и примените его:

~~~bash
curl -fsSLo /tmp/hermes-provider-hardening.patch \
  https://sereja.tech/downloads/hermes-claude-code-cli-provider-hardening.patch

echo "7f2389abd04462df678da2e52b92cf1199a9298cabc6edad3a9bff456d3d242b  /tmp/hermes-provider-hardening.patch" \
  | sha256sum -c -
git -C "$plugin_dir" apply --check /tmp/hermes-provider-hardening.patch
git -C "$plugin_dir" apply /tmp/hermes-provider-hardening.patch
~~~

### 3. Прогнать тесты до реального Opus

~~~bash
cd "$plugin_dir"
python3 -m unittest discover -s tests -v
~~~

На чистой базе с patch у меня прошли 58 тестов. Fake-Claude тесты не расходуют подписочный лимит.

### 4. Настроить loopback shim

Добавьте в ~/.hermes/.env:

~~~dotenv
CLAUDE_CODE_CLI_API_KEY=local
CLAUDE_CODE_CLI_BASE_URL=http://127.0.0.1:8765/v1
CLAUDE_CODE_CLI_AUTOSTART=0
~~~

Значение local — непустой placeholder для registry Hermes. Shim его игнорирует.

Установите managed service из provider:

~~~bash
cd "$plugin_dir"
CLAUDE_CODE_CLI_HOST=127.0.0.1 \
CLAUDE_CODE_CLI_PORT=8765 \
scripts/install-service.sh
~~~

Разрешите user service работать после logout и reboot:

~~~bash
sudo loginctl enable-linger "$(id -un)"
loginctl show-user "$(id -un)" -p Linger
~~~

Ожидаемый результат — Linger=yes.

Дополните ~/.hermes/claude-code-cli-shim.env:

~~~dotenv
CLAUDE_CODE_CLI_BIN=/home/student/.local/bin/claude
CLAUDE_CODE_CLI_MODEL=opus
CLAUDE_CODE_CLI_ENGINE=auto
CLAUDE_CODE_CLI_NATIVE_TOOLS=1
CLAUDE_CODE_CLI_STREAM=1
CLAUDE_CODE_CLI_VISION=1
CLAUDE_CODE_CLI_STRICT_MODEL=1
CLAUDE_CODE_CLI_TIMEOUT=600
~~~

Путь к claude замените на результат command -v claude.

~~~bash
chmod 600 ~/.hermes/.env ~/.hermes/claude-code-cli-shim.env
systemctl --user restart claude-code-cli-shim.service
curl -fsS http://127.0.0.1:8765/healthz
curl -fsS http://127.0.0.1:8765/v1/models
~~~

Закройте SSH, подключитесь снова и повторите health check. Это проверяет работу user service после logout.

### 5. Выбрать provider в Hermes

Через picker:

~~~bash
hermes model
~~~

Выберите claude-code-cli и модель opus. В конфигурации итог должен соответствовать:

~~~yaml
model:
  provider: claude-code-cli
  default: opus
~~~

Теперь проверьте регистрацию provider в Hermes v0.14:

~~~bash
hermes chat -Q --provider claude-code-cli -m opus -q "Reply PROVIDER_OK"
~~~

Этот вызов уже расходует Claude usage.

### 6. Доказать подписочный маршрут

Перед production включением выполните один прямой probe с удалёнными metered и cloud-routing переменными:

~~~bash
env -u ANTHROPIC_API_KEY \
    -u ANTHROPIC_AUTH_TOKEN \
    -u ANTHROPIC_BASE_URL \
    -u CLAUDE_CODE_USE_BEDROCK \
    -u CLAUDE_CODE_USE_VERTEX \
    -u CLAUDE_CODE_USE_FOUNDRY \
  claude -p --model opus \
    --output-format stream-json --verbose \
    "Reply exactly SUBSCRIPTION_OPUS_OK"
~~~

Проверьте apiKeySource, served model и rate-limit event. Остановитесь при isUsingOverage=true, credits required или неожиданном API provider.

После этого прогоните Hermes:

~~~bash
hermes chat -Q --provider claude-code-cli -m opus \
  -q "Reply exactly HERMES_OPUS_OK"
~~~

Отдельно проверьте нативный Hermes tool call и memory roundtrip. Текстовый smoke доказывает только генерацию ответа.

## Переключение Telegram

Перед стартом Hermes остановите gateway, который сейчас использует bot token. Убедитесь, что poller исчез.

Запустите Hermes gateway и проверьте три отдельные ситуации:

1. обычный DM;
2. сообщение внутри Telegram topic;
3. тот же topic после рестарта gateway.

В topic ответ должен ссылаться на входящее сообщение и сохранять topic root. Через Telegram-клиент это видно по reply_to_msg_id, reply_to_top_id и forum_topic=true.

На Hermes v0.14 отдельный Telegram patch мне не понадобился. Живой ответ прошёл внутри topic до и после рестарта.

Финальное состояние моего сервера:

- hermes-gateway.service active/running;
- claude-code-cli-shim.service active/running;
- оба сервиса с NRestarts=0;
- прежний Claude Telegram gateway inactive/dead;
- один Telegram poller;
- agent log: provider claude-code-cli, model opus.

## Промпт для серверного агента

{{< callout insight >}}
Подключи существующий Telegram runtime Hermes к моей подписке Anthropic через официальный Claude Code CLI и user provider.

Сохрани Hermes gateway, sessions, memory и native tool loop. Используй pinned community provider base 09a3aec и только два commit из PR #12: 8e5c74c2 и 62420fb0.

До production сверь SHA-256 versioned hardening patch со страницы и примени его.

Проверь child-env allowlist, host prompt-token accounting и Hermes v0.14 compatibility. Прогони все unit и fake-Claude tests.

Создай backup и точный rollback. Установи официальный Claude Code CLI. Авторизацию выполни через мой Claude plan.

Не печатай credentials и не добавляй Anthropic API key.

Докажи через stream-json: apiKeySource=none, served Opus, subscription rate window и isUsingOverage=false. Остановись при overage, credits required или неизвестном provider.

Подними shim только на 127.0.0.1, managed user service, ENGINE=auto, Hermes native tools, streaming, strict model provenance и timeout 600. Включи linger и проверь сервис после logout.

Проверь Hermes CLI, native tool loop и memory add/remove. Перед Telegram cutover останови текущий poller. Никогда не запускай два poller с одним token.

Проверь отдельными nonce DM, forum topic и forum topic после рестарта. Через Telegram-клиент подтверди source reply, тот же topic root и forum_topic=true.

Покажи финальные service states, NRestarts, единственный poller, provider/model из Hermes agent log и rollback. Продолжай исправлять, пока все проверки не пройдут.
{{< /callout >}}

## Rollback

Сначала остановите Hermes gateway и shim. Пока оба Telegram poller остановлены, восстановите прежний provider и конфиг Hermes.

Claude OAuth refresh credentials ротируются. Если rollback runtime тоже использует Claude Code, сначала передайте ему текущую credential branch и поставьте mode 0600.

После этого запускайте rollback gateway и повторяйте свежие DM/topic smoke. Одновременный запуск двух gateway с одним token создаёт гонку getUpdates.

## Ограничения

Provider поддерживается сообществом. После обновления Hermes, Claude CLI или plugin повторяйте unit, billing, tool, memory, DM, topic и restart проверки.

Каждый turn создаёт процесс claude -p. Это добавляет latency и внутренний prompt floor Claude Code.

Anthropic документирует Claude Code и Agent SDK с подписочным планом. Постоянный owner-only Telegram transport через сторонний Hermes provider остаётся policy gray area.

Публичного одобрения конкретной связки Hermes + Telegram от Anthropic я не нашёл.

Не делитесь consumer credentials и не превращайте личную подписку в multi-user backend.

Похожие серверные связки и агентские отделы я собираю в Personal Corp. [Посмотреть, как это устроено](https://t.me/hashslash_bot?start=pc_blog).

---

## Ссылки

- [Hermes: model providers](https://hermes-agent.nousresearch.com/docs/integrations/providers)
- [Hermes Claude Code CLI provider](https://github.com/Ouroborosrex/hermes-claude-code-cli-provider)
- [Provider issue #13: context accounting](https://github.com/Ouroborosrex/hermes-claude-code-cli-provider/issues/13)
- [Provider PR #12: error handling and model provenance](https://github.com/Ouroborosrex/hermes-claude-code-cli-provider/pull/12)
- [Мой проверенный hardening patch](/downloads/hermes-claude-code-cli-provider-hardening.patch)
- [Claude Code: authentication](https://code.claude.com/docs/en/iam)
- [Claude Code: headless mode](https://code.claude.com/docs/en/headless)
- [Claude Agent SDK with a Claude plan](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan)
- [Claude Code with Pro or Max](https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan)
- [Claude Code legal and compliance](https://code.claude.com/docs/en/legal-and-compliance)
- [Telegram Bot API](https://core.telegram.org/bots/api)
