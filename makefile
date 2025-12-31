include .env
export $(shell sed 's/=.*//' .env)

start:
	@echo "Starting docker containers..."
	@docker compose up -d

stop:
	@make dump
	@echo "Stopping docker containers..."
	@docker compose down -v

restart:
	@make stop
	@make start

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

gen-key:
	@echo "Generating self-signed certificate..."
	@mkdir -p ssl/certs
	@openssl genrsa -out ssl/certs/server.key 4096

	@printf "[req]\n\
	distinguished_name = req_distinguished_name\n\
	x509_extensions = v3_req\n\
	prompt = no\n\
	\n\
	[req_distinguished_name]\n\
	C = PL\n\
	ST = Pomerania\n\
	L = Gdansk\n\
	O = VOL\n\
	OU = Volta:DDDD\n\
	CN = localhost\n\
	\n\
	[v3_req]\n\
	subjectAltName = @alt_names\n\
	\n\
	[alt_names]\n\
	DNS.1 = localhost\n\
	IP.1 = 127.0.0.1\n\
	IP.2 = ::1\n" > ssl/certs/san.cnf

	@openssl req -new -x509 -sha256 \
		-key ssl/certs/server.key \
		-out ssl/certs/server.crt \
		-days 365 \
		-config ssl/certs/san.cnf -extensions v3_req
	@echo "Certificate generated."

