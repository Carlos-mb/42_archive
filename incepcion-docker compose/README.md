*This project has been created as part of the 42 curriculum by cmelero-.*

# Inception

## Description

Inception is a system administration project based on Docker and Docker Compose.

The goal of the project is to deploy a small infrastructure inside a virtual machine. The infrastructure contains three mandatory services, each running in its own dedicated container:

* **NGINX** with TLSv1.2/TLSv1.3 only.
* **WordPress** with PHP-FPM, without NGINX.
* **MariaDB** without NGINX.

The services are built from custom Dockerfiles. Ready-made service images such as `nginx`, `wordpress` or `mariadb` are not used. Each image is built from a Debian base image.

Only the NGINX container is exposed to the host machine through port `443`.

The request flow is:

```text
Browser
  |
  | HTTPS :443
  v
NGINX
  |
  | FastCGI :9000
  v
WordPress / PHP-FPM
  |
  | MariaDB :3306
  v
MariaDB
```

The configured domain name is:

```text
cmelero-.42.fr
```

This domain must resolve to the local machine.

## Project structure

```text
.
├── Makefile
├── README.md
├── USER_DOC.md
├── DEV_DOC.md
├── secrets
│   ├── db_password.txt
│   ├── db_root_password.txt
│   ├── wp_admin_password.txt
│   └── wp_user_password.txt
└── srcs
    ├── .env
    ├── docker-compose.yml
    └── requirements
        ├── mariadb
        │   ├── Dockerfile
        │   ├── conf
        │   │   └── 50-server.cnf
        │   └── tools
        │       └── docker-entrypoint.sh
        ├── nginx
        │   ├── Dockerfile
        │   ├── conf
        │   │   └── default.conf
        │   └── tools
        │       └── docker-entrypoint.sh
        └── wordpress
            ├── Dockerfile
            ├── conf
            │   └── www.conf
            └── tools
                └── docker-entrypoint.sh
```

All files required to configure the infrastructure are placed inside the `srcs` directory. The `Makefile` is located at the root of the repository and builds the complete application using Docker Compose.

## Services

### NGINX

NGINX is the only public entry point of the infrastructure.

It listens on port `443` using TLS only:

```text
443/tcp
```

It does not expose port `80`.

NGINX serves the WordPress files and forwards PHP requests to the WordPress container using FastCGI:

```text
wordpress:9000
```

Configuration file:

```text
srcs/requirements/nginx/conf/default.conf
```

### WordPress

WordPress runs with PHP-FPM.

It listens internally on:

```text
9000/tcp
```

This port is not exposed to the host machine. It is only used by NGINX inside the Docker network.

The WordPress container automatically:

* waits for MariaDB to become available;
* downloads WordPress using WP-CLI;
* creates `wp-config.php`;
* installs WordPress;
* creates one administrator user;
* creates one regular WordPress user.

The WordPress administrator username is:

```text
cmelero_owner
```

It does not contain `admin`, `Admin`, `administrator` or `Administrator`.

The regular WordPress username is:

```text
cmelero_user
```

### MariaDB

MariaDB listens internally on:

```text
3306/tcp
```

This port is not exposed to the host machine. It is only used by WordPress inside the Docker network.

The MariaDB container automatically:

* initializes the database directory if required;
* creates the WordPress database;
* creates the WordPress database user;
* grants the required permissions;
* configures the MariaDB root password.

## Docker images

Each service has its own Dockerfile:

```text
srcs/requirements/nginx/Dockerfile
srcs/requirements/wordpress/Dockerfile
srcs/requirements/mariadb/Dockerfile
```

The Docker images are built by Docker Compose through the Makefile.

The image repository names match their corresponding service names, and each image uses an explicit non-latest tag:

```text
nginx:inception
wordpress:inception
mariadb:inception
```

The `latest` tag is not used.

## Environment variables and secrets

The project uses a `.env` file for non-confidential environment variables:

```text
srcs/.env
```

The `.env` file stores values such as:

* domain name;
* database name;
* database user;
* WordPress title;
* WordPress usernames;
* WordPress emails.

Passwords are not stored in `.env`.

Confidential values are stored in Docker secret files located in:

```text
secrets/
```

Required secret files:

```text
secrets/db_root_password.txt
secrets/db_password.txt
secrets/wp_admin_password.txt
secrets/wp_user_password.txt
```

Purpose of each file:

| File                    | Purpose                                 |
| ----------------------- | --------------------------------------- |
| `db_root_password.txt`  | MariaDB root password                   |
| `db_password.txt`       | Password for the MariaDB WordPress user |
| `wp_admin_password.txt` | WordPress administrator password        |
| `wp_user_password.txt`  | WordPress regular user password         |

These files must exist and must not be empty before running the project.

Credentials must not be hardcoded in:

* Dockerfiles;
* `docker-compose.yml`;
* shell scripts;
* `.env`.

## Volumes and persistence

The project uses two Docker named volumes:

```text
mariadb_data
wordpress_data
```

The named volumes are configured to store their data inside the host directory required by the subject:

```text
/home/cmelero-/data
```

MariaDB data is stored in:

```text
/home/cmelero-/data/mariadb
```

WordPress website files are stored in:

```text
/home/cmelero-/data/wordpress
```

### MariaDB volume

The MariaDB service mounts:

```text
mariadb_data:/var/lib/mysql
```

MariaDB stores its database files in `/var/lib/mysql`.

This volume persists:

* MariaDB internal tables;
* the WordPress database;
* WordPress posts;
* WordPress comments;
* WordPress users;
* WordPress configuration stored in the database.

### WordPress volume

The WordPress service mounts:

```text
wordpress_data:/var/www/html
```

WordPress stores its website files in `/var/www/html`.

This volume persists:

* WordPress core files;
* `wp-config.php`;
* `wp-content`;
* themes;
* plugins;
* uploaded files.

The NGINX service also mounts the WordPress volume, but in read-only mode:

```text
wordpress_data:/var/www/html:ro
```

NGINX only needs to read and serve the WordPress files. It does not need write access.

## Docker network

The project uses a custom Docker network named:

```text
inception
```

All services are connected to this network.

The containers communicate using Docker DNS service names:

```text
nginx -> wordpress:9000
wordpress -> mariadb:3306
```

The project does not use:

* `network: host`;
* `--link`;
* `links`.

Only NGINX is reachable from the host.

## Design choices

### Virtual Machines vs Docker

A virtual machine virtualizes a full operating system, including its own kernel, system services and hardware abstraction. It is heavier but provides strong isolation.

Docker containers share the host kernel and isolate processes, filesystems and networks. Containers are lighter, faster to build, faster to start and better suited for packaging individual services.

This project itself must run inside a virtual machine, but the services inside it are isolated with Docker containers.

### Secrets vs Environment Variables

Environment variables are useful for non-confidential configuration such as service names, database names, usernames and domain names.

Secrets are more appropriate for confidential values such as passwords. In this project, passwords are read from files under `secrets/` and are provided to containers through Docker Compose secrets.

This avoids storing passwords directly in Dockerfiles, scripts, `docker-compose.yml` or `.env`.

### Docker Network vs Host Network

A Docker network isolates the containers from the host and allows services to communicate using service names.

In this project, WordPress can reach MariaDB through:

```text
mariadb:3306
```

NGINX can reach WordPress through:

```text
wordpress:9000
```

Using the host network would remove this isolation and expose more services than necessary. It is also forbidden by the subject.

### Docker Volumes vs Bind Mounts

Docker volumes are managed by Docker and are the standard mechanism for persistent container data.

Bind mounts directly expose an arbitrary host path inside a container. They are useful in development but provide less abstraction and can make a project more dependent on the host filesystem layout.

This project uses Docker named volumes for persistent storage. The named volumes are configured to store their data inside:

```text
/home/cmelero-/data
```

This keeps the required persistence location while still using named volumes in the Docker Compose services.

## Instructions

### Prerequisites

The project must be executed inside a virtual machine.

Docker and Docker Compose must be installed.

The domain must resolve locally. Add this line to `/etc/hosts` if needed:

```text
127.0.0.1 cmelero-.42.fr
```

Command:

```bash
echo "127.0.0.1 cmelero-.42.fr" | sudo tee -a /etc/hosts
```

### Prepare secrets

Before starting the project, create and fill the secret files:

```bash
nano secrets/db_root_password.txt
nano secrets/db_password.txt
nano secrets/wp_admin_password.txt
nano secrets/wp_user_password.txt
chmod 600 secrets/*.txt
```

Each file must contain one non-empty password.

### Build and start

From the repository root:

```bash
make up
```

This command:

* creates the persistent data directories if needed;
* builds the Docker images;
* starts the containers in detached mode.

### Stop

```bash
make down
```

This stops and removes the containers but keeps persistent data.

### Clean

```bash
make clean
```

This stops the stack and removes unused Docker resources.

### Full clean

```bash
make fclean
```

This stops the stack, removes Docker resources and deletes persistent project data from:

```text
/home/cmelero-/data/mariadb
/home/cmelero-/data/wordpress
```

### Rebuild

```bash
make re
```

This performs a full clean and starts the project again.

### Show status

```bash
make ps
```

### Show logs

```bash
make logs
```

## Access

Website:

```text
https://cmelero-.42.fr
```

WordPress administration panel:

```text
https://cmelero-.42.fr/wp-admin
```

WordPress users are configured in:

```text
srcs/.env
```

Passwords are read from:

```text
secrets/wp_admin_password.txt
secrets/wp_user_password.txt
```

## Validation commands

### Check containers

```bash
make ps
```

Expected services:

```text
nginx
wordpress
mariadb
```

### Check HTTPS

```bash
curl -k -I https://cmelero-.42.fr
```

Expected result:

```text
HTTP/1.1 200 OK
```

### Check exposed ports

```bash
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

Expected state:

```text
nginx       0.0.0.0:443->443/tcp, [::]:443->443/tcp
wordpress   9000/tcp
mariadb     3306/tcp
```

Only NGINX must publish a host port.

### Check host listening ports

```bash
sudo ss -tulpn | grep -E ':(80|443|3306|9000)\b' || true
```

Only port `443` should be listening on the host for this project.

### Check WordPress installation

```bash
docker exec wordpress wp core is-installed --path=/var/www/html --allow-root && echo "OK: WordPress installed"
docker exec wordpress wp user list --path=/var/www/html --allow-root
```

Expected users:

```text
cmelero_owner   administrator
cmelero_user    author
```

### Check MariaDB

```bash
docker exec mariadb mariadb -uroot --password="$(cat secrets/db_root_password.txt)" -e "SELECT User, Host FROM mysql.user;"
docker exec mariadb mariadb -uroot --password="$(cat secrets/db_root_password.txt)" -e "SHOW DATABASES;"
```

Expected state:

```text
wpuser@%
wordpress database
```

## Persistence test

1. Start the project:

```bash
make up
```

2. Open the WordPress website:

```text
https://cmelero-.42.fr
```

3. Create a WordPress comment.

4. Stop the project:

```bash
make down
```

5. Start the project again:

```bash
make up
```

6. Confirm that the comment still exists.

7. Reboot the virtual machine:

```bash
sudo reboot
```

8. After reboot, check the stack:

```bash
cd ~/inception
make ps
curl -k -I https://cmelero-.42.fr
```

9. Check the WordPress comments:

```bash
docker exec wordpress wp comment list --path=/var/www/html --allow-root --fields=comment_ID,comment_content,comment_approved
```

The comment must still exist after restart and reboot.

## Resources

Classic documentation and references used for this project:

* Docker documentation: https://docs.docker.com/
* Docker Compose documentation: https://docs.docker.com/compose/
* Dockerfile reference: https://docs.docker.com/reference/dockerfile/
* Docker volumes documentation: https://docs.docker.com/engine/storage/volumes/
* Docker networking documentation: https://docs.docker.com/engine/network/
* Docker secrets documentation: https://docs.docker.com/compose/how-tos/use-secrets/
* NGINX documentation: https://nginx.org/en/docs/
* PHP-FPM documentation: https://www.php.net/manual/en/install.fpm.php
* MariaDB documentation: https://mariadb.com/kb/en/documentation/
* WordPress documentation: https://developer.wordpress.org/
* WP-CLI documentation: https://wp-cli.org/

AI assistance was used during the project as a support tool for:

* planning the Docker Compose architecture;
* checking whether the service separation matched the subject;
* reviewing Dockerfile and entrypoint structure;
* debugging initialization issues during MariaDB and WordPress startup;
* drafting documentation;
* preparing validation commands for the peer evaluation.

All generated suggestions were manually reviewed, tested and adapted before being included in the project.
