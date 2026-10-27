FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

RUN useradd --create-home --uid 10001 appuser
USER appuser

# Trusted proxy for X-Forwarded-For: uvicorn reads FORWARDED_ALLOW_IPS natively.
# Never a wildcard (clients could spoof their IP past the anon rate limit). Coolify sets the Traefik IP/subnet.
ENV FORWARDED_ALLOW_IPS=127.0.0.1
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:8080/health')" || exit 1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers"]
