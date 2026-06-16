#!/bin/sh
set -eu

read_secret() {
    file="$1"

    if [ ! -f "$file" ]; then
        echo "Missing secret file: $file" >&2
        exit 1
    fi

    value="$(tr -d '\r\n' < "$file")"

    if [ -z "$value" ]; then
        echo "Empty secret file: $file" >&2
        exit 1
    fi

    printf '%s' "$value"
}

require_env() {
    var_name="$1"
    eval "value=\${$var_name:-}"

    if [ -z "$value" ]; then
        echo "Missing environment variable: $var_name" >&2
        exit 1
    fi
}

require_env DOMAIN_NAME
require_env WORDPRESS_DB_HOST
require_env WORDPRESS_DB_NAME
require_env WORDPRESS_DB_USER
require_env WORDPRESS_TITLE
require_env WORDPRESS_ADMIN_USER
require_env WORDPRESS_ADMIN_EMAIL
require_env WORDPRESS_USER
require_env WORDPRESS_USER_EMAIL
require_env WORDPRESS_USER_ROLE

WORDPRESS_DB_PASSWORD="$(read_secret /run/secrets/db_password)"
WORDPRESS_ADMIN_PASSWORD="$(read_secret /run/secrets/wp_admin_password)"
WORDPRESS_USER_PASSWORD="$(read_secret /run/secrets/wp_user_password)"

mkdir -p /run/php /var/www/html
chown -R www-data:www-data /run/php /var/www/html

cd /var/www/html

rm -f /var/www/html/index.nginx-debian.html

echo "Waiting for MariaDB..."
for i in $(seq 1 60); do
    if mariadb-admin ping \
        -h"${WORDPRESS_DB_HOST}" \
        -u"${WORDPRESS_DB_USER}" \
        --password="${WORDPRESS_DB_PASSWORD}" \
        --silent > /dev/null 2>&1; then
        break
    fi
    sleep 1
done

if ! mariadb-admin ping \
    -h"${WORDPRESS_DB_HOST}" \
    -u"${WORDPRESS_DB_USER}" \
    --password="${WORDPRESS_DB_PASSWORD}" \
    --silent > /dev/null 2>&1; then
    echo "MariaDB is not available" >&2
    exit 1
fi

if [ ! -f /var/www/html/wp-settings.php ]; then
    echo "Downloading WordPress..."
    wp core download \
        --path=/var/www/html \
        --allow-root

    chown -R www-data:www-data /var/www/html
fi

if [ ! -f /var/www/html/wp-config.php ]; then
    echo "Creating wp-config.php..."
    wp config create \
        --path=/var/www/html \
        --dbname="${WORDPRESS_DB_NAME}" \
        --dbuser="${WORDPRESS_DB_USER}" \
        --dbpass="${WORDPRESS_DB_PASSWORD}" \
        --dbhost="${WORDPRESS_DB_HOST}:3306" \
        --allow-root

    chown www-data:www-data /var/www/html/wp-config.php
fi

if ! wp core is-installed --path=/var/www/html --allow-root > /dev/null 2>&1; then
    echo "Installing WordPress..."
    wp core install \
        --path=/var/www/html \
        --url="https://${DOMAIN_NAME}" \
        --title="${WORDPRESS_TITLE}" \
        --admin_user="${WORDPRESS_ADMIN_USER}" \
        --admin_password="${WORDPRESS_ADMIN_PASSWORD}" \
        --admin_email="${WORDPRESS_ADMIN_EMAIL}" \
        --skip-email \
        --allow-root
fi

if ! wp user get "${WORDPRESS_USER}" --path=/var/www/html --allow-root > /dev/null 2>&1; then
    echo "Creating WordPress regular user..."
    wp user create \
        "${WORDPRESS_USER}" \
        "${WORDPRESS_USER_EMAIL}" \
        --path=/var/www/html \
        --user_pass="${WORDPRESS_USER_PASSWORD}" \
        --role="${WORDPRESS_USER_ROLE}" \
        --allow-root
fi

chown -R www-data:www-data /var/www/html

exec "$@"
