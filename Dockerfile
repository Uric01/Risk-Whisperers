FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Replace risk_whisperers.wsgi with your Django project's WSGI module if needed.
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn ${DJANGO_WSGI_MODULE:-risk_whisperers.wsgi}:application --bind 0.0.0.0:8000"]