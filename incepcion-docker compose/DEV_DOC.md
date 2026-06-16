# Developer Documentation

## Purpose

This document explains how a developer can set up, build, launch and manage the Inception project from scratch.

It covers:

* prerequisites;
* configuration files;
* secret files;
* Makefile commands;
* Docker Compose commands;
* container management;
* volume management;
* persistent data location.

## Architecture

The project deploys three services:

```text
NGINX      -> public HTTPS entry point on port 443
WordPress  -> internal PHP-FPM service on port 9000
MariaDB    -> internal database service on port 3306
```

Request flow:

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

Only NGINX exposes a port to the host machine.

WordPress and MariaDB are reachable only inside the Docker network.

## Repository structure

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

## Prerequisites

The project must run inside a virtual machine.

Required packages:

```bash
sudo apt update
sudo apt install -y git make curl ca-certificates gnupg lsb-release openssh-server vim tree
```

Docker and Docker Compose plugin must be installed.

Example installation on Debian:

```bash
sudo install -m 0755 -d /etc/apt/keyrings

sudo curl -fsSL https://download.docker.com/linux/debian/gpg \
  -o /etc/apt/keyrings/docker.asc

sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Enable Docker:

```bash
sudo systemctl enable --now docker
```

Allow the current user to run Docker commands:

```bash
sudo usermod -aG docker "$USER"
```

After this command, log out and log in again, or reboot the virtual machine.

Verify Docker:

```bash
docker --version
docker compose version
docker run hello-world
```

## Domain configuration

The project domain is:

```text
cmelero-.42.fr
```

It must resolve to the local machine.

Add this line to `/etc/hosts` if it is not already present:

```text
127.0.0.1 cmelero-.42.fr
```

Command:

```bash
echo "127.0.0.1 cmelero-.42.fr" | sudo tee -a /etc/hosts
```

## Configuration files

### Docker Compose file

Main Compose file:

```text
srcs/docker-compose.yml
```

It defines:

* the `nginx` service;
* the `wordpress` service;
* the `mariadb` service;
* the `inception` Docker network;
* the `mariadb_data` named volume;
* the `wordpress_data` named volume;
* Docker secrets.

### Environment file

Non-secret variables are stored in:

```text
srcs/.env
```

This file contains configuration such as:

* domain name;
* WordPress database name;
* WordPress database user;
* WordPress title;
* WordPress usernames;
* WordPress emails.

Passwords must not be stored in `.env`.

### Service configuration files

NGINX configuration:

```text
srcs/requirements/nginx/conf/default.conf
```

WordPress PHP-FPM configuration:

```text
srcs/requirements/wordpress/conf/www.conf
```

MariaDB configuration:

```text
srcs/requirements/mariadb/conf/50-server.cnf
```

### Entrypoint scripts

Each service has an entrypoint script:

```text
srcs/requirements/nginx/tools/docker-entrypoint.sh
srcs/requirements/wordpress/tools/docker-entrypoint.sh
srcs/requirements/mariadb/tools/docker-entrypoint.sh
```

The entrypoint scripts prepare each container before starting the main service process.

NGINX entrypoint:

* generates a self-signed TLS certificate if needed;
* starts NGINX.

WordPress entrypoint:

* reads secrets;
* waits for MariaDB;
* downloads WordPress;
* creates `wp-config.php`;
* installs WordPress;
* creates the WordPress administrator user;
* creates the WordPress regular user;
* starts PHP-FPM.

MariaDB entrypoint:

* reads secrets;
* initializes MariaDB if required;
* creates the WordPress database;
* creates the MariaDB WordPress user;
* grants permissions;
* configures the MariaDB root password;
* starts MariaDB.

## Secrets

Secret files are stored in:

```text
secrets/
```

Required files:

```text
secrets/db_root_password.txt
secrets/db_password.txt
secrets/wp_admin_password.txt
secrets/wp_user_password.txt
```

Purpose:

| File                    | Purpose                                          |
| ----------------------- | ------------------------------------------------ |
| `db_root_password.txt`  | MariaDB root password                            |
| `db_password.txt`       | Password used by WordPress to connect to MariaDB |
| `wp_admin_password.txt` | WordPress administrator password                 |
| `wp_user_password.txt`  | WordPress regular user password                  |

Create or edit the secret files manually:

```bash
nano secrets/db_root_password.txt
nano secrets/db_password.txt
nano secrets/wp_admin_password.txt
nano secrets/wp_user_password.txt
```

Each file must contain one non-empty password.

Set permissions:

```bash
chmod 600 secrets/*.txt
```

Secrets must not be hardcoded in:

* Dockerfiles;
* `docker-compose.yml`;
* `.env`;
* shell scripts;
* documentation examples with real credentials.

## Build and launch with Makefile

All Makefile commands must be executed from the repository root:

```bash
cd ~/inception
```

### Start the project

```bash
make up
```

This command:

* creates persistent data directories if needed;
* builds the Docker images;
* starts all services in detached mode.

Equivalent Docker Compose command:

```bash
docker compose -f srcs/docker-compose.yml up -d --build
```

### Stop the project

```bash
make down
```

This stops and removes the containers, but keeps persistent data.

Equivalent Docker Compose command:

```bash
docker compose -f srcs/docker-compose.yml down
```

### Show status

```bash
make ps
```

Equivalent Docker Compose command:

```bash
docker compose -f srcs/docker-compose.yml ps
```

### Show logs

```bash
make logs
```

Equivalent Docker Compose command:

```bash
docker compose -f srcs/docker-compose.yml logs -f
```

### Clean unused Docker resources

```bash
make clean
```

This stops the project and removes unused Docker resources.

### Full clean

```bash
make fclean
```

This stops the project, removes Docker resources and deletes persistent project data from:

```text
/home/cmelero-/data/mariadb
/home/cmelero-/data/wordpress
```

Use this command carefully because it resets the WordPress installation and database.

### Rebuild from scratch

```bash
make re
```

This runs a full clean and starts the project again.

## Docker Compose management commands

Validate the Compose file:

```bash
docker compose -f srcs/docker-compose.yml config
```

Build images:

```bash
docker compose -f srcs/docker-compose.yml build
```

Start containers:

```bash
docker compose -f srcs/docker-compose.yml up -d
```

Stop containers:

```bash
docker compose -f srcs/docker-compose.yml down
```

Show containers:

```bash
docker compose -f srcs/docker-compose.yml ps
```

Show logs:

```bash
docker compose -f srcs/docker-compose.yml logs
```

Follow logs:

```bash
docker compose -f srcs/docker-compose.yml logs -f
```

Restart one service:

```bash
docker compose -f srcs/docker-compose.yml restart nginx
docker compose -f srcs/docker-compose.yml restart wordpress
docker compose -f srcs/docker-compose.yml restart mariadb
```

Rebuild one service:

```bash
docker compose -f srcs/docker-compose.yml build nginx
docker compose -f srcs/docker-compose.yml build wordpress
docker compose -f srcs/docker-compose.yml build mariadb
```

Start one service after rebuilding:

```bash
docker compose -f srcs/docker-compose.yml up -d --build nginx
docker compose -f srcs/docker-compose.yml up -d --build wordpress
docker compose -f srcs/docker-compose.yml up -d --build mariadb
```

## Container management

List running containers:

```bash
docker ps
```

List all containers:

```bash
docker ps -a
```

Inspect container logs:

```bash
docker logs nginx
docker logs wordpress
docker logs mariadb
```

Open a shell inside a container:

```bash
docker exec -it nginx sh
docker exec -it wordpress sh
docker exec -it mariadb sh
```

Check WordPress installation:

```bash
docker exec wordpress wp core is-installed --path=/var/www/html --allow-root
```

List WordPress users:

```bash
docker exec wordpress wp user list --path=/var/www/html --allow-root
```

List WordPress comments:

```bash
docker exec wordpress wp comment list --path=/var/www/html --allow-root --fields=comment_ID,comment_content,comment_approved
```

Check MariaDB databases:

```bash
docker exec mariadb mariadb -uroot --password="$(cat secrets/db_root_password.txt)" -e "SHOW DATABASES;"
```

Check MariaDB users:

```bash
docker exec mariadb mariadb -uroot --password="$(cat secrets/db_root_password.txt)" -e "SELECT User, Host FROM mysql.user;"
```

## Volume management

The project uses two Docker named volumes:

```text
mariadb_data
wordpress_data
```

List volumes:

```bash
docker volume ls
```

Inspect MariaDB volume:

```bash
docker volume inspect mariadb_data
```

Inspect WordPress volume:

```bash
docker volume inspect wordpress_data
```

Remove stopped containers while keeping volumes:

```bash
make down
```

Remove project data completely:

```bash
make fclean
```

Manual removal of persistent project data:

```bash
sudo rm -rf /home/cmelero-/data/mariadb
sudo rm -rf /home/cmelero-/data/wordpress
```

Manual removal should only be used when intentionally resetting the project.

## Persistent data location

The subject requires persistent data to be stored under:

```text
/home/cmelero-/data
```

This project stores MariaDB data in:

```text
/home/cmelero-/data/mariadb
```

This project stores WordPress files in:

```text
/home/cmelero-/data/wordpress
```

The Compose file defines named volumes backed by these host paths:

```yaml
volumes:
  mariadb_data:
    name: mariadb_data
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /home/cmelero-/data/mariadb

  wordpress_data:
    name: wordpress_data
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /home/cmelero-/data/wordpress
```

MariaDB service mount:

```yaml
volumes:
  - mariadb_data:/var/lib/mysql
```

WordPress service mount:

```yaml
volumes:
  - wordpress_data:/var/www/html
```

NGINX service mount:

```yaml
volumes:
  - wordpress_data:/var/www/html:ro
```

NGINX uses the WordPress volume in read-only mode because it only needs to read and serve the files.

## What persists

### MariaDB persistence

MariaDB stores its data inside the container at:

```text
/var/lib/mysql
```

This path is persisted through the `mariadb_data` volume.

It stores:

* MariaDB internal tables;
* the `wordpress` database;
* WordPress posts;
* WordPress comments;
* WordPress users;
* WordPress options;
* database permissions.

### WordPress persistence

WordPress stores its files inside the container at:

```text
/var/www/html
```

This path is persisted through the `wordpress_data` volume.

It stores:

* WordPress core files;
* `wp-config.php`;
* `wp-content`;
* themes;
* plugins;
* uploads.

## Persistence behavior

The following commands do not delete persistent data:

```bash
make down
docker compose -f srcs/docker-compose.yml down
```

The containers are removed, but the data remains in:

```text
/home/cmelero-/data/mariadb
/home/cmelero-/data/wordpress
```

The following command deletes persistent project data:

```bash
make fclean
```

After `make fclean`, WordPress and MariaDB are initialized again on the next `make up`.

## Validation from scratch

From a clean virtual machine:

1. Install prerequisites and Docker.
2. Copy or clone the repository.
3. Configure `/etc/hosts`.
4. Create and fill the secret files.
5. Run:

```bash
cd ~/inception
make up
```

6. Check containers:

```bash
make ps
```

7. Check HTTPS:

```bash
curl -k -I https://cmelero-.42.fr
```

Expected result:

```text
HTTP/1.1 200 OK
```

8. Check exposed ports:

```bash
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

Expected state:

```text
nginx       0.0.0.0:443->443/tcp, [::]:443->443/tcp
wordpress   9000/tcp
mariadb     3306/tcp
```

Only NGINX must expose a host port.

9. Check host listening ports:

```bash
sudo ss -tulpn | grep -E ':(80|443|3306|9000)\b' || true
```

Only port `443` should be listening on the host for this project.

## Developer notes

* Do not expose MariaDB to the host.
* Do not expose WordPress to the host.
* Do not use `network: host`.
* Do not use `links`.
* Do not hardcode passwords in Dockerfiles, scripts, `.env` or `docker-compose.yml`.
* Do not use ready-made service images for NGINX, WordPress or MariaDB.
* Rebuild the project with `make re` when testing a full clean initialization.
* Use `make down` when testing persistence without deleting data.
* Use `make fclean` only when intentionally resetting all persistent project data.
