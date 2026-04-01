FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

RUN python manage.py collectstatic --noinput 2>/dev/null || true

RUN python manage.py migrate --run-syncdb 2>/dev/null || true
RUN python manage.py seed_data 2>/dev/null || true

EXPOSE 3000

CMD ["sh", "-c", "python manage.py migrate --run-syncdb && python manage.py seed_data && gunicorn config.wsgi:application --bind 0.0.0.0:3000 --workers 2 --timeout 120"]
