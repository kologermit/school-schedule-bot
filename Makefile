dev_push:
	git add .
	EDITOR=nano && git commit
	git push origin $$(git branch --show-current)
venv:
	rm -rf ./venv
	python3 -m venv ./venv
	./venv/bin/pip install -r ./requirements.txt
.env:
	rm -f ./.env
	cp ./.env.example ./.env
	nano ./.env


# Управление сервисом скачивания
bot_logs:
	docker compose logs --tail 20 -f bot
bot_logs0:
	docker compose logs --tail 0 -f bot
bot_run:
	docker compose up -d bot 
	make bot_logs0
bot_stop:
	docker compose stop bot
bot_remove:
	docker compose rm -sfv bot
bot_restart:
	docker compose restart bot 
	make bot_logs0
bot_force_recreate:
	docker compose up -d --force-recreate --build bot
	make bot_logs0
bot_exec:
	docker compose exec bot sh


# Упарвление базой
db_logs:
	docker compose logs --tail 20 -f db
db_logs0:
	docker compose logs --tail 0 -f db
db_run:
	docker compose up -d db
	make db_logs0
db_force_recreate:
	docker compose up -d --force-recreate db
	make db_logs0
db_remove_data:
	docker compose rm -sfv db bot
	docker volume rm school-schedule-bot_db-data
	docker compose up -d db
db_exec:
	docker compose exec db bash


# Управление всеми контейнерами
all_logs:
	docker compose logs --tail 20 -f 
all_logs0:
	docker compose logs --tail 0 -f
all_run:
	docker compose up -d
	make all_logs0
all_restart:
	docker compose restart
	make all_logs0
all_force_recreate:
	docker compose up -d --force-recreate --build
	make all_logs0
all_stop:
	docker compose stop
all_remove:
	docker compose rm -sfv