NAME := codexion

CC := cc
CFLAGS := -Wall -Wextra -Werror -pthread
RM := rm -f

SRC := \
	codexion_log.c \
	codexion_main.c \
	codexion_parse_config.c \
	codexion_queues.c \
	codexion_setup.c \
	codexion_setup_impl.c \
	codexion_state.c \
	codexion_threads.c \
	codexion_threads_impl.c \
	ft_dongle_functions.c \
	codexion_generic.c \
	ft_dongle_setup.c \
	ft_time_functions.c

OBJ := $(SRC:.c=.o)

all: $(NAME)

$(NAME): $(OBJ)
	$(CC) $(CFLAGS) $(OBJ) -o $(NAME)

%.o: %.c codexion.h
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	$(RM) $(OBJ)

fclean: clean
	$(RM) $(NAME)

re: fclean all

.PHONY: all clean fclean re
