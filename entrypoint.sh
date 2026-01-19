#!/bin/bash
set -e

FILE="/var/www/html/app/config/parameters.php"
if [ -f "$FILE" ]; then
    echo "Aktualizacja pliku parameters.php..."
    sed -i "s/'database_host' => '.*'/'database_host' => '$DB_SERVER'/g" "$FILE"
    sed -i "s/'database_name' => '.*'/'database_name' => '$DB_NAME'/g" "$FILE"
    sed -i "s/'database_user' => '.*'/'database_user' => '$DB_USER'/g" "$FILE"
    sed -i "s/'database_password' => '.*'/'database_password' => '$DB_PASSWD'/g" "$FILE"
    sed -i "s/'database_port' => '.*'/'database_port' => '$DB_PORT'/g" "$FILE"
fi

HTACCESS_FILE="/var/www/html/.htaccess"
if [ -f "$HTACCESS_FILE" ]; then
    echo "Podmiana wszystkich portów na $PUBLISHED_PORT w .htaccess..."
    sed -i "s/8443/$PUBLISHED_PORT/g" "$HTACCESS_FILE"
fi

exec apache2-foreground