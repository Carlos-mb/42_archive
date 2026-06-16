# User Documentation

## Purpose

This document explains how to use and administer the Inception stack.

It covers:

* what services are provided;
* how to start and stop the project;
* how to access the website and the WordPress administration panel;
* where credentials are stored;
* how to check that the services are running correctly.

## Provided services

The stack provides three services:

### NGINX

NGINX is the public entry point of the project.

It listens on HTTPS port:

```text
443
```

Users access the website through NGINX.

NGINX forwards PHP requests internally to the WordPress container.

### WordPress

WordPress provides the website and the administration panel.

It runs internally with PHP-FPM on port:

```text
9000
```

This port is not exposed to the host machine. It is only used internally by NGINX.

### MariaDB

MariaDB stores the WordPress database.

It runs internally on port:

```text
3306
```

This port is not exposed to the host machine. It is only used internally by WordPress.

## Public access

The public website is available at:

```text
https://cmelero-.42.fr
```

The WordPress administration panel is available at:

```text
https://cmelero-.42.fr/wp-admin
```

If the domain does not resolve, add this line to `/etc/hosts` on the virtual machine:

```text
127.0.0.1 cmelero-.42.fr
```

Command:

```bash
echo "127.0.0.1 cmelero-.42.fr" | sudo tee -a /etc/hosts
```

## Credentials

Credentials are stored in the `secrets` directory.

Required files:

```text
secrets/db_root_password.txt
secrets/db_password.txt
secrets/wp_admin_password.txt
secrets/wp_user_password.txt
```

Meaning of each file:

| File                    | Purpose                                          |
| ----------------------- | ------------------------------------------------ |
| `db_root_password.txt`  | MariaDB root password                            |
| `db_password.txt`       | Password used by WordPress to connect to MariaDB |
| `wp_admin_password.txt` | WordPress administrator password                 |
| `wp_user_password.txt`  | WordPress regular user password                  |

The files must exist and must not be empty before starting the project.

To edit them:

```bash
nano secrets/db_root_password.txt
nano secrets/db_password.txt
nano secrets/wp_admin_password.txt
nano secrets/wp_user_password.txt
```

Then set secure permissions:

```bash
chmod 600 secrets/*.txt
```

Passwords are not stored in:

* `docker-compose.yml`;
* Dockerfiles;
* `.env`;
* shell scripts.

## WordPress users

The WordPress users are created automatically during the first initialization.

Configured usernames:

```text
Administrator: cmelero_owner
Regular user:  cmelero_user
```

Passwords are read from:

```text
secrets/wp_admin_password.txt
secrets/wp_user_password.txt
```

Important: changing the secret files after WordPress has already been installed does not automatically change existing WordPress passwords.

To change WordPress passwords after installation, use the WordPress administration panel or WP-CLI.

## Persistent data

Persistent data is stored on the host machine in:

```text
/home/cmelero-/data
```

MariaDB data is stored in:

```text
/home/cmelero-/data/mariadb
```

WordPress files are stored in:

```text
/home/cmelero-/data/wordpress
```

This means that posts, comments, users and WordPress files survive container restarts and `make down`.

## Starting the project

Run all commands from the repository root:

```bash
cd ~/inception
```

Start the stack:

```bash
make up
```

This command:

* creates the persistent data directories if needed;
* builds the Docker images;
* starts the containers in detached mode.

## Stopping the project

Stop the stack:

```bash
make down
```

This stops and removes the containers, but keeps persistent data.

The WordPress data and MariaDB database remain available when the stack is started again.

## Rebuilding the project

To rebuild the whole project from scratch:

```bash
make re
```

This removes persistent project data and starts the stack again.

Use this only when you want to reset the installation.

## Cleaning

Remove unused Docker resources:

```bash
make clean
```

Full clean:

```bash
make fclean
```

`make fclean` removes containers, Docker resources and the persistent data stored in:

```text
/home/cmelero-/data/mariadb
/home/cmelero-/data/wordpress
```

Use it carefully because it deletes the WordPress installation and database.

## Checking the services

Show the current containers:

```bash
make ps
```

Expected services:

```text
nginx
wordpress
mariadb
```

Show logs:

```bash
make logs
```

Check that the website responds:

```bash
curl -k -I https://cmelero-.42.fr
```

Expected result:

```text
HTTP/1.1 200 OK
```

Check exposed ports:

```bash
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

Expected result:

```text
nginx       0.0.0.0:443->443/tcp, [::]:443->443/tcp
wordpress   9000/tcp
mariadb     3306/tcp
```

Only NGINX must publish a port to the host.

WordPress and MariaDB must not expose host ports.

Check host listening ports:

```bash
sudo ss -tulpn | grep -E ':(80|443|3306|9000)\b' || true
```

For this project, only port `443` should be publicly listening on the host.

## Checking WordPress

Check that WordPress is installed:

```bash
docker exec wordpress wp core is-installed --path=/var/www/html --allow-root && echo "OK: WordPress installed"
```

List WordPress users:

```bash
docker exec wordpress wp user list --path=/var/www/html --allow-root
```

Expected users:

```text
cmelero_owner
cmelero_user
```

## Checking MariaDB

Check MariaDB users:

```bash
docker exec mariadb mariadb -uroot --password="$(cat secrets/db_root_password.txt)" -e "SELECT User, Host FROM mysql.user;"
```

Check databases:

```bash
docker exec mariadb mariadb -uroot --password="$(cat secrets/db_root_password.txt)" -e "SHOW DATABASES;"
```

Expected database:

```text
wordpress
```

Expected WordPress database user:

```text
wpuser
```

## Persistence test

To verify persistence:

1. Start the stack:

```bash
make up
```

2. Open the website:

```text
https://cmelero-.42.fr
```

3. Create a WordPress comment.

4. Stop the stack:

```bash
make down
```

5. Start the stack again:

```bash
make up
```

6. Open the website again and confirm that the comment still exists.

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

9. Check WordPress comments:

```bash
docker exec wordpress wp comment list --path=/var/www/html --allow-root --fields=comment_ID,comment_content,comment_approved
```

The comment should still exist after stopping the stack and after rebooting the virtual machine.

## Common problems

### The website does not open

Check containers:

```bash
make ps
```

Check logs:

```bash
make logs
```

Check HTTPS:

```bash
curl -k -I https://cmelero-.42.fr
```

### The domain does not resolve

Add the domain to `/etc/hosts`:

```bash
echo "127.0.0.1 cmelero-.42.fr" | sudo tee -a /etc/hosts
```

### WordPress cannot connect to MariaDB

Check MariaDB users:

```bash
docker exec mariadb mariadb -uroot --password="$(cat secrets/db_root_password.txt)" -e "SELECT User, Host FROM mysql.user;"
```

Check that the `wordpress` database exists:

```bash
docker exec mariadb mariadb -uroot --password="$(cat secrets/db_root_password.txt)" -e "SHOW DATABASES;"
```

### A secret file is empty

Edit the required file:

```bash
nano secrets/db_root_password.txt
nano secrets/db_password.txt
nano secrets/wp_admin_password.txt
nano secrets/wp_user_password.txt
```

Then restart the stack:

```bash
make down
make up
```
