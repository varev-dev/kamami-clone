#!/bin/bash

PREFIX="BE_198020"
DB_NAME="BE_198020"
DB_USER="root"
DB_PASS="student"
DB_HOST="admin-mysql_db"
PORT="19802"
COMPOSE_FILE="docker-compose.yml"

echo "Usuwanie starego stacka: $PREFIX..."
docker stack rm $PREFIX
echo "Czekam 20s na zwolnienie zasobów sieciowych..."
sleep 20

echo "Wdrażanie stacka $PREFIX..."
docker stack deploy -c $COMPOSE_FILE $PREFIX --with-registry-auth

echo "Szukanie kontenera Prestashop..."
PS_CONTAINER=""
for i in {1..60}; do
    RUNNING=$(docker service ps ${PREFIX}_prestashop \
    --filter "desired-state=running" \
    --format '{{.CurrentState}}' | grep -c Running)

    if [ "$RUNNING" -gt 0 ]; then
        echo "Serwis Prestashop działa!"
        break
    fi

    echo "Próba $i/60: Serwis jeszcze nie działa..."
    sleep 5
    if [ $i -eq 60 ]; then
        echo "Serwis nie wystartował w wyznaczonym czasie"
        break
    fi
done

echo "Inicjalizacja bazy danych z dump.sql..."

DB_CONTAINER=$(docker ps -q -f name=admin-mysql_db)

if [ ! -z "$DB_CONTAINER" ]; then
    echo "Usuwanie bazy danych $DB_NAME (jeśli istnieje)..."
    docker exec -i $DB_CONTAINER mysql -u$DB_USER -p$DB_PASS -e "DROP DATABASE IF EXISTS \`$DB_NAME\`;"

    echo "Tworzenie bazy danych $DB_NAME"
    docker exec -i $DB_CONTAINER mysql -u$DB_USER -p$DB_PASS -e "CREATE DATABASE IF NOT EXISTS \`$DB_NAME\`;"

    echo "Import dump.sql do bazy $DB_NAME..."
    docker exec -i $DB_CONTAINER mysql -u$DB_USER -p$DB_PASS $DB_NAME < dump.sql
    echo "Baza została zainicjalizowana."

    echo "Aktualizacja adresów URL sklepu w bazie danych..."
    docker exec -i $DB_CONTAINER mysql -u$DB_USER -p$DB_PASS $DB_NAME <<EOF
UPDATE ps_configuration SET value='localhost:$PORT' WHERE name IN ('PS_SHOP_DOMAIN', 'PS_SHOP_DOMAIN_SSL');
UPDATE ps_shop_url SET domain='localhost:$PORT', domain_ssl='localhost:$PORT';
EOF
    echo "Adresy URL w bazie zaktualizowane na localhost:$PORT"
else
    echo "Ostrzeżenie: Nie znaleziono kontenera admin-mysql_db na tym węźle. Skrypt nie mógł zainicjalizować bazy."
fi

echo "-------------------------------------------------------"
echo "GOTOWE! Sklep powinien być dostępny pod adresem:"
echo "http://localhost:$PORT"
echo "Pamiętaj o aktywnym tunelu SSH!"