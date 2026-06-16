COMPOSE_FILE = srcs/docker-compose.yml
DATA_DIR = /home/cmelero-/data

.PHONY: all up down clean fclean re ps logs

all: up

up:
	mkdir -p $(DATA_DIR)/mariadb $(DATA_DIR)/wordpress
	docker compose -f $(COMPOSE_FILE) up -d --build

down:
	docker compose -f $(COMPOSE_FILE) down

clean: down
	docker system prune -af

fclean: down
	docker system prune -af --volumes
	sudo rm -rf $(DATA_DIR)/mariadb $(DATA_DIR)/wordpress

re: fclean up

ps:
	docker compose -f $(COMPOSE_FILE) ps

logs:
	docker compose -f $(COMPOSE_FILE) logs -f
