#!/bin/sh

alembic upgrade heads
celery call tasks.update_currency
uvicorn main:app --host 0.0.0.0 --port "9000"
