COMPOSE_FILE=docker-compose.yml

docker-run:
	docker-compose -f ${COMPOSE_FILE} up -d

docker-clean:
	docker-compose -f ${COMPOSE_FILE} down

docker-respawn:
	docker rm -f mongodb && docker-compose -f ${COMPOSE_FILE} up -d mongodb

static-test:
	pipenv run type-check

test:
	$(MAKE) static-test
	set -a && . ./.env && pipenv run test

run-local:
	set -a && . ./.env && pipenv run main

auto-format:
	pipenv run ruff-fix
	pipenv run ruff-format
	pipenv run ruff