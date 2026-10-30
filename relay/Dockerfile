# Wake relay (ADR-0011): own image and Coolify app. Build from the relay/ directory:
#   docker build -t mmbridge-relay:bs1 relay
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY relay.py .

# /data: persistent volume for the dedupe db (relay.db); owned by the app user, private.
RUN useradd --create-home --uid 10001 appuser && mkdir -p /data && chown 10001:10001 /data && chmod 700 /data
USER appuser

ENV FORWARDED_ALLOW_IPS=127.0.0.1
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:8080/health')" || exit 1
CMD ["uvicorn", "relay:create_app", "--factory", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers"]
