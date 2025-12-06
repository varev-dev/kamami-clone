include .env
export $(shell sed 's/=.*//' .env)

start:
	@echo "Starting docker containers..."
	@docker compose up -d

stop:
	@make dump
	@echo "Stopping docker containers..."
	@docker compose down

permissions:
	@echo "Changing ownership to www-data..."
	sudo chown -R 33:33 ./prestashop
	sudo chmod -R 775 ./prestashop
	@echo "Checking if user is in www-data group..."
	@if ! id -nG "$$(whoami)" | grep -qw "www-data"; then \
		echo "Adding user to www-data group..."; \
		sudo usermod -a -G www-data "$$(whoami)"; \
		newgrp www-data; \
	else \
		echo "User already in www-data group."; \
	fi

dump:
	@echo "Dumping config into ./new_dump.sql"
	docker exec prestashop-mysql mysqldump prestashop --user=root -p$(MYSQL_ROOT_PASSWORD) -x > new_dump.sql