SHELL := /bin/bash

up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f api

psql:
	docker exec -it ai-pipeworks-postgres psql -U app -d app

