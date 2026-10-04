# Booking система переговорних кімнат

Сервіс для бронювання переговорних кімнат в офісі.

**Стек:** Python 3.12, FastAPI, PostgreSQL, SQLAlchemy 2.0, Alembic, Docker Compose.

## Запуск через Docker

```bash
cp .env.example .env    # за потреби змінити пароль
docker-compose up -d --build
```

Під час старту контейнер API автоматично застосовує міграції (`alembic upgrade head`): створюються таблиці та додаються 3 кімнати.

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

## Локальний запуск (без Docker)

Потрібен запущений PostgreSQL та база з параметрами з `.env` (`DATABASE_URL` з хостом `localhost`).

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

## Ендпоінти

| Метод | Шлях | Опис | Відповіді |
|---|---|---|---|
| GET | `/api/rooms` | Список кімнат | 200 |
| POST | `/api/bookings` | Створити бронювання | 201, 400 (перетин), 404 (кімнати немає), 422 (невалідний час) |
| GET | `/api/bookings?room_id=1&date=2026-10-05` | Список бронювань, обидва фільтри необов'язкові | 200 |
| DELETE | `/api/bookings/{booking_id}` | Скасувати бронювання | 204, 404 |

Приклад тіла `POST /api/bookings`:

```json
{
  "room_id": 1,
  "organizer_name": "Ivan",
  "start_time": "2026-10-05T10:00:00Z",
  "end_time": "2026-10-05T11:00:00Z"
}
```

Час передається з часовим поясом (`Z` або `+03:00`), інакше 422.

## Бізнес-правила

- **Валідація (422).** На рівні Pydantic-схеми перевіряється, що `start_time` не в минулому, а `end_time` строго більший за `start_time`.
- **Перетин (400).** Кімнату не можна забронювати, якщо інтервал перетинається з наявним бронюванням цієї кімнати. Умова перетину: `existing.start < new.end AND existing.end > new.start`. Бронювання «впритул» (10:00–11:00 і 11:00–12:00) дозволені.
- **Фільтр за датою** повертає бронювання, що починаються в цю дату (UTC).

## Архітектура

```
app/
  routers/       # HTTP-шар: лише приймає запит і викликає сервіс
  services/      # бізнес-логіка: перевірка перетину, 400/404
  repositories/  # робота з БД (SQLAlchemy)
  schemas/       # Pydantic-схеми та валідація
  models/        # SQLAlchemy-моделі
  dependencies.py  # DI: сесія → репозиторії → сервіс через Depends()
alembic/         # міграції (таблиці + початкові кімнати)
```
