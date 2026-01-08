# Wczytaj zmienne z pliku .env w folderze config
include config/.env
export $(shell sed 's/=.*//' config/.env)

# Definicja komendy docker compose ze wskazaniem na pliki konfiguracyjne
# --project-directory . sprawia, że ścieżki w compose (np. ../data) są liczone od głównego katalogu
COMPOSE = docker compose -f config/docker-compose.yml --env-file config/.env --project-directory .

.PHONY: start stop restart permissions dump gen-key help

help:
	@echo "Dostępne komendy:"
	@echo "  make start       - Uruchamia kontenery (build + detach)"
	@echo "  make stop        - Zatrzymuje kontenery i robi backup bazy"
	@echo "  make restart     - Restartuje środowisko"
	@echo "  make permissions - Naprawia uprawnienia do folderu sources"
	@echo "  make dump        - Tworzy zrzut bazy do data/dump.sql"
	@echo "  make gen-key     - Generuje certyfikaty SSL w config/ssl"

start:
	@echo "Starting docker containers..."
	@$(COMPOSE) up -d --build

stop:
	@make dump
	@echo "Stopping docker containers..."
	@$(COMPOSE) down

restart:
	@make stop
	@make start

permissions:
	@echo "Changing ownership of sources to www-data..."
	sudo chown -R 33:33 ./sources
	sudo chmod -R 775 ./sources
	@echo "Checking if user is in www-data group..."
	@if ! id -nG "$$(whoami)" | grep -qw "www-data"; then \
		echo "Adding user to www-data group..."; \
		sudo usermod -a -G www-data "$$(whoami)"; \
		newgrp www-data; \
	else \
		echo "User already in www-data group."; \
	fi

dump:
	@echo "Dumping database into data/dump.sql..."
	@mkdir -p data
	docker exec prestashop-mysql mysqldump $(MYSQL_DATABASE) --user=root -p$(MYSQL_ROOT_PASSWORD) > data/dump.sql
	@echo "Backup saved to data/dump.sql"

gen-key:
	@echo "Generating self-signed certificate in config/ssl..."
	@mkdir -p config/ssl/certs
	@openssl genrsa -out config/ssl/certs/server.key 4096

	@printf "[req]\n\
	distinguished_name = req_distinguished_name\n\
	x509_extensions = v3_req\n\
	prompt = no\n\
	\n\
	[req_distinguished_name]\n\
	C = PL\n\
	ST = Pomerania\n\
	L = Gdansk\n\
	O = KamamiClone\n\
	OU = Development\n\
	CN = localhost\n\
	\n\
	[v3_req]\n\
	subjectAltName = @alt_names\n\
	\n\
	[alt_names]\n\
	DNS.1 = localhost\n\
	IP.1 = 127.0.0.1\n\
	IP.2 = ::1\n" > config/ssl/certs/san.cnf

	@openssl req -new -x509 -sha256 \
		-key config/ssl/certs/server.key \
		-out config/ssl/certs/server.crt \
		-days 365 \
		-config config/ssl/certs/san.cnf -extensions v3_req
	@echo "Certificate generated."
