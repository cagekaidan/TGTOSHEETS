# Telegram Bot для Google Sheets

Бот для Telegram, который позволяет добавлять данные в Google Sheets через простой интерфейс с кнопками.

## Возможности

- Последовательный ввод данных: Телефон → Email → Имя → Тип
- Возможность пропуска любого поля
- Автоматическое сохранение в Google Sheets
- Валидация телефонов и email
- Простой интерфейс с кнопками

## Структура таблицы

| Телефон | Email | Имя | Тайп |
|---------|-------|-----|------|
| ...     | ...   | ... | ...  |

## Настройка

### 1. Переменные окружения

Необходимо настроить следующие переменные:

- `TELEGRAM_BOT_TOKEN` - токен бота от @BotFather
- `GOOGLE_SHEETS_ID` - ID Google таблицы
- `GOOGLE_SERVICE_ACCOUNT_JSON` - JSON с ключами сервисного аккаунта

### 2. Google Sheets API

1. Создайте проект в Google Cloud Console
2. Включите Google Sheets API
3. Создайте сервисный аккаунт
4. Скачайте JSON файл с ключами
5. Предоставьте доступ к таблице сервисному аккаунту

### 3. Telegram Bot

1. Напишите @BotFather в Telegram
2. Создайте бота командой /newbot
3. Получите токен

## Запуск

```bash
pip install python-telegram-bot gspread google-auth google-auth-oauthlib google-auth-httplib2
python main.py
```

## Файлы проекта

- `main.py` - основной файл бота
- `config.py` - конфигурация и настройки
- `sheets_manager.py` - работа с Google Sheets
- `validators.py` - валидация данных
- `bot_states.py` - состояния пользователей