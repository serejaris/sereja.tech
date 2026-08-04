---
title: "Как подключить подписку Anthropic к Hermes с помощью агента"
date: 2026-08-04
description: "Понятная инструкция без ручной настройки: скопируйте готовый промпт серверному агенту, войдите в Anthropic и проверьте ответы Hermes в Telegram."
tags: ["hermes", "anthropic", "claude-code", "telegram", "вайбкодинг"]
image: "/images/blog/claude-max-hermes-telegram-preview.png"
cta: personal_corp
cta_code: pc_blog
---

Если у вас уже работает Hermes-бот, его можно подключить к Opus через действующую подписку Anthropic.

Самостоятельно разбираться в сервере, командах и настройках не потребуется. Ниже есть готовое задание для агента.

Вам не придётся вводить команды в терминале. Скопируйте задание целиком и дождитесь результатов проверки.

Я прошёл этот путь на живом боте. Hermes сохранил память, скиллы и Telegram. Opus отвечает через мою подписку Claude. Extra Usage остался выключен.

## Что получится

После настройки вы продолжите писать прежнему Telegram-боту.

Hermes останется основой бота. Он сохранит свои диалоги, память, скиллы и инструменты. Ответы модели будет готовить Opus через официальный Claude Code.

Вам не понадобится Anthropic API key. Оплата за отдельные API-запросы тоже не подключается.

Мой тест выполнен на Claude Max. Подойдёт платный план Anthropic, который даёт доступ к Claude Code и нужной модели. Доступность Opus агент проверит до переключения бота.

## Что потребуется от вас

Подготовьте четыре вещи:

1. Работающий Hermes-бот.
2. Доступ агента к серверу с Hermes.
3. Активную подписку Anthropic с Claude Code.
4. Доступ к Telegram для финальной проверки.

Подойдёт Codex, Claude Code или другой серверный агент, который умеет работать по SSH, читать логи, менять конфиги и запускать тесты.

Если агент уже устанавливал или обслуживал ваш Hermes, используйте тот же чат. Доступ к серверу у него, скорее всего, уже настроен.

Пароль Anthropic, OAuth-токены и Telegram bot token агенту отправлять не нужно.

## Шаг 1. Дайте агенту готовое задание

Откройте агента, у которого есть доступ к серверу Hermes.

Можно отправить ему ссылку на эту статью и попросить выполнить готовое задание:

~~~text
Прочитай эту статью целиком и выполни задание из раздела Шаг 1:
https://sereja.tech/blog/claude-max-hermes-telegram/

Работай до полного результата и используй все проверки из статьи.
~~~

Скопируйте весь блок ниже одним сообщением. Текст внутри рассчитан на агента. Вам не нужно понимать команды, названия файлов и технические проверки.

~~~text
Подключи мой существующий Telegram-бот Hermes к Opus через мою действующую подписку Anthropic.

Главный результат: Hermes остаётся runtime бота, сохраняет свои сессии, память, скиллы и native tools. Каждый основной ответ модели идёт через официальный Claude Code CLI и мою подписочную сессию.

Работай самостоятельно до полного результата. Остановись только для моего входа в Anthropic, необратимого действия или реального блокера после трёх попыток исправления.

Сначала изучи текущий сервер, версию Hermes, конфиги, systemd services, Telegram gateway, активные poller и доступные backup. Прочитай локальные AGENTS.md и runbooks.

Перед изменениями проверь актуальность решения через официальную документацию, GitHub и Grok CLI. Сопоставь публичные данные с текущим сервером.

Не заменяй Hermes официальным Claude Telegram Channel. Нужен Hermes с user model provider, который запускает официальный claude -p локально.

Используй проверенную основу:
https://github.com/Ouroborosrex/hermes-claude-code-cli-provider

Base commit:
09a3aec0ab7406c6a0731f858f1b4b7a99f0cb77

Добавь два commit из PR #12 в указанном порядке:
8e5c74c2eb3017fd47f5d1d504625d3c87058b40
62420fb094a1124292bd4931781b45a8e7ab9633

Примени проверенный hardening patch:
https://sereja.tech/downloads/hermes-claude-code-cli-provider-hardening.patch

Ожидаемый SHA-256:
7f2389abd04462df678da2e52b92cf1199a9298cabc6edad3a9bff456d3d242b

Перед production создай внешний backup и отдельную копию конфигов Hermes. Запиши точный rollback. Сохрани текущий рабочий gateway как выключенный резерв.

Сначала проверь provider в изолированном окружении. Прогони все unit tests и fake-Claude Hermes smokes. Ожидается 58 тестов без ошибок.

Проверь совместимость user provider с установленной версией Hermes. Для Hermes v0.14 учти отсутствие поля supports_vision в старой схеме ProviderProfile.

Установи официальный Claude Code CLI на целевой сервер. Авторизацию выполни от имени service account Hermes.

Когда потребуется вход в Anthropic, покажи мне только ссылку или код авторизации и дождись моего подтверждения. Не печатай и не передавай credentials.

Не добавляй Anthropic API key. Не включай Extra Usage. Не меняй billing.

Перед реальным запросом удали из окружения дочернего claude все metered и cloud-routing переменные.

В subprocess не должны попадать ANTHROPIC_API_KEY, ANTHROPIC_AUTH_TOKEN, ANTHROPIC_BASE_URL, Bedrock, Vertex, Foundry, Telegram token и ключи других провайдеров.

Разреши только системные переменные, настройки локальной подписочной сессии Claude Code и явно необходимые параметры.

Докажи подписочный маршрут через claude auth status и stream-json probe.

Прими результат только при одновременном выполнении условий:
- authMethod сообщает claude.ai;
- apiProvider сообщает firstParty;
- apiKeySource сообщает none;
- реально обслужившая модель относится к Opus;
- isUsingOverage=false;
- нет credits required;
- нет неожиданного API provider.

Подними provider shim только на 127.0.0.1. Не создавай публичный порт, DNAT или новое firewall rule.

Используй managed systemd user service. Включи streaming, Hermes native tools, strict model provenance, engine=auto и timeout 600.

Включи linger для service account. Проверь, что сервис остаётся активным после logout и restart.

Настрой Hermes на provider claude-code-cli и модель opus.

Проверь по отдельности:
- обычный текстовый ответ;
- native Hermes tool call;
- добавление и удаление временной memory-записи;
- доступность нужных скиллов;
- корректную модель и provider в agent log.

Перед Telegram cutover останови прежний gateway. Один bot token должен обслуживать ровно один poller.

После запуска Hermes отправь свежие уникальные сообщения и проверь:
- ответ в обычном DM;
- ответ внутри существующего Telegram topic;
- ответ в том же topic после рестарта Hermes gateway;
- повторный DM после рестарта.

Для topic проверь через Telegram-клиент:
- ответ ссылается на исходное сообщение;
- reply_to_top_id совпадает с корнем topic;
- forum_topic=true.

Реакция с глазами без текстового ответа не считается успехом.

Финальный отчёт должен содержать:
- Hermes gateway active/running;
- Claude CLI shim active/running;
- NRestarts=0;
- Linger=yes;
- ровно один Telegram poller;
- прежний gateway inactive;
- provider claude-code-cli;
- model opus;
- isUsingOverage=false;
- результаты DM, topic и restart;
- путь к backup и команды rollback.

Claude OAuth refresh credentials могут ротироваться. Перед rollback в другой container сначала синхронизируй туда текущую credential branch, пока оба Telegram gateway остановлены.

Не показывай мне секреты. Не удаляй пользовательские данные. Не запускай два gateway с одним Telegram token.

Продолжай диагностировать и исправлять, пока все проверки не пройдут.
~~~

## Шаг 2. Войдите в Anthropic

Во время работы агент попросит авторизовать Claude Code.

Он должен прислать ссылку или короткий код. Откройте ссылку, войдите в свой аккаунт Anthropic и подтвердите доступ.

После успешного входа напишите агенту: готово.

Пароль, содержимое файла credentials и OAuth-токен отправлять в чат нельзя. Агенту достаточно увидеть статус успешной авторизации на сервере.

## Шаг 3. Проверьте бота в Telegram

После отчёта агента выполните три простых проверки.

### Обычный диалог

Напишите боту:

~~~text
Ответь ровно: ЛИЧКА РАБОТАЕТ
~~~

Бот должен прислать эту фразу ответом на ваше сообщение.

### Диалог внутри topic

Откройте существующий topic и напишите:

~~~text
Ответь ровно: ТОПИК РАБОТАЕТ
~~~

Ответ должен появиться внутри того же topic.

### Проверка после перезапуска

Попросите агента перезапустить Hermes gateway. Затем повторите сообщение внутри topic.

Если бот поставил реакцию и промолчал, проверка провалена. Отправьте агенту:

~~~text
После рестарта бот ставит реакцию и молчит в topic. Продолжай диагностику. Проверь единственный poller, agent log, reply_to_top_id и forum_topic. Не останавливайся до текстового ответа внутри этого же topic.
~~~

## Как понять, что всё готово

Работа завершена, когда агент показал шесть подтверждений:

1. Hermes и вспомогательный сервис активны.
2. В логах указаны Opus и provider claude-code-cli.
3. Подписка используется с isUsingOverage=false.
4. В Telegram работает обычный диалог.
5. Ответ приходит внутрь topic до и после рестарта.
6. Сохранены backup и понятный rollback.

Скрин статуса сервисов сам по себе ничего не доказывает. Главная проверка — реальные ответы бота в Telegram.

## Что происходит внутри

Hermes продолжает принимать сообщения, помнить контекст и запускать свои инструменты.

Небольшой локальный адаптер передаёт запрос официальному Claude Code. Claude Code использует вашу подписочную сессию и возвращает ответ Hermes.

Эта часть полностью поручена агенту. Человеку достаточно пройти авторизацию и проверить Telegram.

## Важное ограничение

Связка рассчитана на личного бота владельца подписки.

Anthropic официально поддерживает Claude Code с платными планами. Постоянная работа через сторонний Hermes provider остаётся серой зоной правил.

Не передавайте свою подписку другим людям и не превращайте её в общий сервис.

Похожие серверные связки и агентские отделы я собираю в Personal Corp. [Посмотреть, как это устроено](https://t.me/hashslash_bot?start=pc_blog).

---

## Ссылки для агента

- [Hermes: model providers](https://hermes-agent.nousresearch.com/docs/integrations/providers)
- [Hermes Claude Code CLI provider](https://github.com/Ouroborosrex/hermes-claude-code-cli-provider)
- [Проверенный hardening patch](/downloads/hermes-claude-code-cli-provider-hardening.patch)
- [Claude Code: вход и авторизация](https://code.claude.com/docs/en/iam)
- [Claude Code: headless mode](https://code.claude.com/docs/en/headless)
- [Claude Agent SDK с подпиской](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan)
- [Claude Code с Pro или Max](https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan)
- [Правила использования Claude Code](https://code.claude.com/docs/en/legal-and-compliance)
