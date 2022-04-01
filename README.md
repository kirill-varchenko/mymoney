# MyMoney

**MyMoney** is my pet project consisting of 3 parts:

1. Postgres database with accounts/transactions tables and summary views.
2. Django service with summary html view and DB admin app.
3. Telegram bot for quick expense inputs.

For docker-compose .env file with DB_NAME, DB_USER and DB_PASSWORD should be in the project root folder. For bot additional .env file with BOT_TOKEN and MY_USER_ID (for filtering inputs from other users) should be in ./bot/ folder.

External Docker volume for the database should be created before the first run:
```bash
docker volume create --name=money_db
```
SQL init script is db/init.sql

To run the project use:
```bash
docker-compose up --build
```

Used tools:

- Django
- Django ORM
- Postgres
- SQLAlchemy
- pydantic
- python-telegram-bot
- Docker