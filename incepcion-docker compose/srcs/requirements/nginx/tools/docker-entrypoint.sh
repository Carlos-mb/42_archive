#!/bin/sh
set -eu

DOMAIN_NAME="${DOMAIN_NAME:-cmelero-.42.fr}"

mkdir -p /etc/nginx/ssl

if [ ! -f /etc/nginx/ssl/inception.crt ] || [ ! -f /etc/nginx/ssl/inception.key ]; then
    echo "Generating self-signed TLS certificate for ${DOMAIN_NAME}..."

    openssl req -x509 -nodes -days 365 \
        -newkey rsa:4096 \
        -keyout /etc/nginx/ssl/inception.key \
        -out /etc/nginx/ssl/inception.crt \
        -subj "/C=ES/ST=Madrid/L=Madrid/O=42/OU=Inception/CN=${DOMAIN_NAME}"

    chmod 600 /etc/nginx/ssl/inception.key
    chmod 644 /etc/nginx/ssl/inception.crt
fi

exec "$@"
