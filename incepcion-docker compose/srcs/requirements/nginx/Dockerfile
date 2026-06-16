FROM debian:bookworm

RUN apt update \
    && apt install -y --no-install-recommends nginx openssl \
    && rm -rf /var/lib/apt/lists/*

COPY conf/default.conf /etc/nginx/conf.d/default.conf
COPY tools/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

RUN chmod +x /usr/local/bin/docker-entrypoint.sh \
    && rm -f /etc/nginx/sites-enabled/default \
    && mkdir -p /etc/nginx/ssl /var/www/html

EXPOSE 443

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
