### Инструкция по установке Telegram MedBot

## Необходимая версия Python: 3.10+

После выполнения команды `git clone` вам необходимо создать виртуальное окружение:
`python3 -m venv env`

Следующим шагом необходимо запустить виртуальное окружение:
`source env/bin/activate`

Далее необходимо установить все зависимости:
`pip install -r requirements.txt`

После установки зависимостей необходимо указать значение токена для телграм бота и путь к базе данных в переменные виртуальной среды:
Unix:
1. `export BOT_TOKEN="..."`
2. `export DB_PATH="..."`
Windows:
1. `SET BOT_TOKEN="..."`
2. `SET DB_PATH="..."`

После установки переменных виртуальный среды необходимо запустить файл для генерации данных в базе данных:
`python3 generate_db.py`

После генерации базы данных можно запустить бота следующей командой:
`python3 bot.py`

# Бот успешно запущен!
