# saloon_bot — карта проекта

Telegram-бот для записи клиентов на маникюр/педикюр (мастер Алеся Матюшева, Минск). Записи хранятся в Google Calendar (events) и в SQLite. Развёрнут через Docker.

## Стек
- Python 3, `pyTelegramBotAPI` (telebot) — Telegram API
- `google-api-python-client` — Google Calendar API (service account)
- `sqlite3` — локальная БД
- `pandas` — чтение прайса/процедур из `.xlsx`
- `portion` — интервалы времени (окна/занятость)
- `schedule` — фоновые задачи

## Запуск
- Локально: `python saloon_bot.py` (нужен `credentials.py` с ключами, см. ниже)
- Docker: `docker build -t saloon_bot .` затем `docker run -e PYTHONUNBUFFERED=1 --restart=unless-stopped -d saloon_bot`

## Файлы (по важности)

| Файл | Назначение |
|------|-----------|
| `saloon_bot.py` | Точка входа. Регистрация `@bot.message_handler`/`@bot.callback_query_handler`, диалоги регистрации/записи, `bot.infinity_polling()` |
| `g_funcs.py` | Класс `Google_calendar` — вся работа с Google Calendar: окна, брони, статистика, расстановка окон (`place_windows`). Экземпляр `clndr`, `calendar_id_1/2` |
| `db_handler.py` | Класс `DB_handler` (sqlite3). Таблицы `clients`, `visits`, `procedures`. Глобальный объект `db` |
| `bot_funcs.py` | Вспомогательные: валидация телефона/имени, `scheduled_tasks`, `get_available_times`, `reply_bookings`, `read_config` |
| `keyboards.py` | Все клавиатуры (главное меню, админ, выбор дат/времени, подтверждение/отмена записи) |
| `ru_dates.py` | Русские названия дней/месяцев, конвертация дат |
| `client.py` | Класс `Client` (состояние клиента в памяти: flag, chosen_procedure_id, admin и т.д.) |
| `user_data/messages.py` | Тексты сообщений (константы `ABOUT`, `BOT_CAN_DO`, и т.д.) |
| `user_data/g_config.json` | Креды service account Google |
| `user_data/procedures.xlsx` | Прайс/расписание процедур (загружается в БД) |
| `user_data/price.xlsx` | Прайс-лист |
| `procedures.json` | Ключи-названия процедур + `av_price`, `timing` (обновляется из статистики) |
| `config.json` | Параметры `general`: имя БД, дни показа окон, цвета событий календаря |
| `db_test.py`, `test.ipynb` | Отладка/тесты |

## Отсутствующие/генерируемые файлы
- `credentials.py` — НЕ в репо (в `.gitignore`), содержит `admin_ids`, `admin_usernames`, `apikey` (токен Telegram). Создаётся вручную.
- `saloon.sqlite` — БД, создаётся при запуске (`db.setup()` вызывается в `db_handler.py`).
- `backups/` — бэкапы БД (ежедневно + при рестарте).

## Ключевые потоки
1. **Регистрация клиента**: `/start` → «Записаться» → если нового, через флаги `Client.flag` (`проверить телефон`, `проверить имя`) → `db.add_client`.
2. **Запись**: выбор процедуры → `clndr.get_available_times` (окна из календаря) → выбор дня/времени → `clndr.occupy_window` (бронь окна) → подтверждение `confirm_book` → `db.add_visit` + `clndr.add_visit`.
3. **Фоновые задачи** (`bf.scheduled_tasks`, отдельный поток): ежедневный бэкап БД (02:00), очистка старых бэкапов, сброс просроченных броней `clndr.reset_occupations` (каждую минуту), обновление `av_price` в начале месяца, heartbeat.
4. **Статистика/окна** (админ): команда `admino` → `Показать статистику` (`clndr.show_stats`), `Выгрузить окна` (`clndr.show_windows`).

## Формат callback_data (Telegram inline-кнопки)
- `procedure_id=<id>` — выбор процедуры
- `day=<ru_day>` — выбор дня
- `daytime&<day>&<time>` — выбор времени
- `confirm_book&<proc_id>&<date>&<time>` — подтверждение
- `c=<booking_id>` / `d=<id>` / `k=<id>` — отмена записи
- `stats_shift=<n>` / `windows_shift=<n>` — месяц статистики/окон

## Важные детали
- Две календарные почты: `calendar_id_1 = 'voffanich@gmail.com'`, `calendar_id_2 = 'kazlova.alesia@gmail.com'` (используется в ботах).
- Логика записи привязана к событиям Google Calendar с `summary` = `'Окно'` (свободно) / `'Бронь с <datetime>'` (зарезервировано) / имя клиента + цена (запись). `description` события хранит telegram_id/телефон/процедуру.
- `Client`-объекты хранятся в dict `clients` по `user_id`, пересоздаются из БД при старте (`bf.create_client_objects_from_db`).
- Часовой пояс: `+03:00` / `Europe/Minsk`.
- Токен-экономия: при изменениях сначала читать конкретный файл из этой таблицы, а не весь проект.
