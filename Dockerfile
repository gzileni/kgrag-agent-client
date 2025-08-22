FROM python:3.12-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt || true

RUN pip install --no-cache-dir uv

COPY *.py .

EXPOSE 8010

ENV PYTHONUNBUFFERED=1

ENV UVICORN_HOST=0.0.0.0
ENV UVICORN_PORT=8020
ENV UVICORN_LOG_LEVEL=debug
ENV UVICORN_WORKERS=1

ENTRYPOINT ["sh", "-c", "uvicorn main:app --host=$UVICORN_HOST --port=$UVICORN_PORT --log-level=$UVICORN_LOG_LEVEL --workers=$UVICORN_WORKERS"]
