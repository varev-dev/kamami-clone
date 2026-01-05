include ../../.env
export $(shell sed 's/=.*//' ../../.env)

delete-products:
	@echo "Deleting all products and images..."
	@docker exec -i prestashop-mysql sh -c 'echo "DELETE FROM ps_category_product; \
DELETE FROM ps_product_lang; \
DELETE FROM ps_product_shop; \
DELETE FROM ps_product_sale; \
DELETE FROM ps_stock_available; \
DELETE FROM ps_product_tag; \
DELETE FROM ps_product_attribute_combination; \
DELETE FROM ps_product_attribute_shop; \
DELETE FROM ps_product_attribute; \
DELETE FROM ps_product; \
ALTER TABLE ps_product AUTO_INCREMENT = 1; \
ALTER TABLE ps_stock_available AUTO_INCREMENT = 1; \
ALTER TABLE ps_product_attribute AUTO_INCREMENT = 1;" | mysql -uroot -p$(MYSQL_ROOT_PASSWORD) prestashop'
	@echo "All products and images deleted."

delete-categories:
	@echo "Deleting categories..."
	@docker exec -i prestashop-mysql sh -c 'echo "DELETE FROM ps_category_product WHERE id_category NOT IN (1,2); \
DELETE FROM ps_category_group WHERE id_category NOT IN (1, 2); \
DELETE FROM ps_category_lang WHERE id_category NOT IN (1,2); \
DELETE FROM ps_category_shop WHERE id_category NOT IN (1,2); \
DELETE FROM ps_category WHERE id_category NOT IN (1,2); \
ALTER TABLE ps_category AUTO_INCREMENT = 3;" | mysql -uroot -p$(MYSQL_ROOT_PASSWORD) prestashop'
	@echo "Categories deleted."

delete-images:
	@echo "Deleting all product images..."
	@docker exec -i prestashop-mysql sh -c 'echo "\
DELETE FROM ps_image_lang; \
DELETE FROM ps_image_shop; \
DELETE FROM ps_image; \
ALTER TABLE ps_image AUTO_INCREMENT = 1;" | mysql -uroot -p$(MYSQL_ROOT_PASSWORD) prestashop'
	@echo "All images deleted."

clean-all: delete-images delete-products delete-categories
	@echo "Database cleaned: all images, products and categories removed."