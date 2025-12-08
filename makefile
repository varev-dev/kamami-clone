include .env
export $(shell sed 's/=.*//' .env)

start:
	@echo "Starting docker containers..."
	@docker compose up -d

stop:
	@make dump
	@echo "Stopping docker containers..."
	@docker compose down -v

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

delete-products:
	@echo "Deleting all products and images..."
	@docker exec -i prestashop-mysql sh -c 'echo "DELETE FROM ps_category_product; \
DELETE FROM ps_product_lang; \
DELETE FROM ps_product_shop; \
DELETE FROM ps_product_sale; \
DELETE FROM ps_stock_available; \
DELETE FROM ps_product_tag; \
DELETE FROM ps_image_lang; \
DELETE FROM ps_image_shop; \
DELETE FROM ps_image; \
DELETE FROM ps_product_attribute_combination; \
DELETE FROM ps_product_attribute_shop; \
DELETE FROM ps_product_attribute; \
DELETE FROM ps_product; \
ALTER TABLE ps_product AUTO_INCREMENT = 1; \
ALTER TABLE ps_image AUTO_INCREMENT = 1; \
ALTER TABLE ps_stock_available AUTO_INCREMENT = 1; \
ALTER TABLE ps_product_attribute AUTO_INCREMENT = 1;" | mysql -uroot -p$(MYSQL_ROOT_PASSWORD) prestashop'
	@echo "All products and images deleted."

delete-categories:
	@echo "Deleting categories..."
	@docker exec -i prestashop-mysql sh -c 'echo "DELETE FROM ps_category_product WHERE id_category NOT IN (1,2); \
DELETE FROM ps_category_lang WHERE id_category NOT IN (1,2); \
DELETE FROM ps_category_shop WHERE id_category NOT IN (1,2); \
DELETE FROM ps_category WHERE id_category NOT IN (1,2);" | mysql -uroot -p$(MYSQL_ROOT_PASSWORD) prestashop'
	@echo "Categories deleted."

clean-all: delete-products delete-categories
	@echo "Database cleaned: all products and categories removed."