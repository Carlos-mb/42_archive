# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cmelero- <cmelero-@student.42madrid.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/01/21 10:15:00 by cmelero-          #+#    #+#              #
#    Updated: 2026/01/21 10:15:00 by cmelero-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = push_swap
CC = cc
CFLAGS = -Wall -Werror -Wextra
SRC = 	push_swap.c \
		push_swap_utils.c \
		push_swap_lst.c \
		push_swap_simple.c \
		push_swap_movement_push.c \
		push_swap_movement_swap.c \
		push_swap_bench.c \
		push_swap_radix.c \
		push_swap_adaptive.c \
		push_swap_medium.c \
		push_swap_more_utils.c

OBJ = $(SRC:.c=.o)
INCLUDE = push_swap.h
LIBFT_DIR = libft
LIBFT = $(LIBFT_DIR)/libft.a
RM = rm -f

.PHONY: all clean fclean re

all: $(NAME)

$(NAME): $(OBJ) $(LIBFT)
	$(CC) $(CFLAGS) $(OBJ) -L$(LIBFT_DIR) -lft -o $(NAME)

$(LIBFT):
	$(MAKE) -C $(LIBFT_DIR)
	@test -f $(LIBFT)

%.o: %.c $(INCLUDE)
	$(CC) $(CFLAGS) -I. -I$(LIBFT_DIR) -c $< -o $@

clean:
	$(RM) $(OBJ)
	$(MAKE) -C $(LIBFT_DIR) clean

fclean: clean
	$(RM) $(NAME)
	$(MAKE) -C $(LIBFT_DIR) fclean

re: fclean all
