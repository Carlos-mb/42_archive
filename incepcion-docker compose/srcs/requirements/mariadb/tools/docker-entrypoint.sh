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

require_env MYSQL_DATABASE
require_env MYSQL_USER

MYSQL_ROOT_PASSWORD="$(read_secret /run/secrets/db_root_password)"
MYSQL_PASSWORD="$(read_secret /run/secrets/db_password)"

mkdir -p /run/mysqld /var/lib/mysql
chown -R mysql:mysql /run/mysqld /var/lib/mysql

if [ ! -d /var/lib/mysql/mysql ]; then
    echo "Creating MariaDB system tables..."

    mariadb-install-db \
        --user=mysql \
        --datadir=/var/lib/mysql \
        --skip-test-db > /dev/null
fi

if [ ! -f /var/lib/mysql/.inception_initialized ]; then
    echo "Initializing Inception database and users..."

    mariadbd \
        --user=mysql \
        --datadir=/var/lib/mysql \
        --socket=/run/mysqld/mysqld.sock \
        --pid-file=/run/mysqld/mysqld.pid \
        --skip-networking &

    temp_pid="$!"

    for i in $(seq 1 30); do
        if mariadb-admin --socket=/run/mysqld/mysqld.sock ping > /dev/null 2>&1; then
            break
        fi
        sleep 1
    done

    if ! mariadb-admin --socket=/run/mysqld/mysqld.sock ping > /dev/null 2>&1; then
        echo "MariaDB temporary server failed to start" >&2
        exit 1
    fi

    mariadb --socket=/run/mysqld/mysqld.sock -u root <<SQL
DELETE FROM mysql.user WHERE User='';
DROP DATABASE IF EXISTS test;
CREATE DATABASE IF NOT EXISTS \`${MYSQL_DATABASE}\` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'%' IDENTIFIED BY '${MYSQL_PASSWORD}';
GRANT ALL PRIVILEGES ON \`${MYSQL_DATABASE}\`.* TO '${MYSQL_USER}'@'%';
ALTER USER 'root'@'localhost' IDENTIFIED BY '${MYSQL_ROOT_PASSWORD}';
FLUSH PRIVILEGES;
SQL

    touch /var/lib/mysql/.inception_initialized
    chown mysql:mysql /var/lib/mysql/.inception_initialized

    mariadb-admin \
        --socket=/run/mysqld/mysqld.sock \
        -u root \
        --password="${MYSQL_ROOT_PASSWORD}" \
        shutdown

    wait "$temp_pid" || true

    echo "MariaDB Inception initialization completed."
fi

exec "$@"
