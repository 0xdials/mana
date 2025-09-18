# mana

minimal AI/ML infra skeleton — postgres, redis, fastapi

## layout

ai-pipeworks/
├── .env
├── .gitignore
├── docker-compose.yml
├── Makefile
├── pgdata/ # postgres data (gitignored)
└── api/
├── Dockerfile
├── main.py
└── requirements.txt


## usage
```sh
# start stack
docker-compose up -d --build

# follow api logs
docker-compose logs -f api

# check health
curl -s localhost:8080/healthz

example response:

{
  "ok": true,
  "postgres": true,
  "redis": true,
  "service": "mana",
  "ts": 1699999999
}

env vars

Set in .env at repo root:

    PG_DSN → Postgres connection string (default: postgresql://app:app@postgres:5432/app)

    REDIS_URL → Redis connection string (default: redis://redis:6379/0)

These values are injected into the API container at runtime.
notes

    data lives in ./pgdata (gitignored)

    make up / make down for quick start/stop

    api listens on :8080, postgres on :5432, redis on :6379
