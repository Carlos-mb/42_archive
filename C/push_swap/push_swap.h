/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/21 09:48:52 by cmelero-          #+#    #+#             */
/*   Updated: 2026/02/06 18:25:32 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# define ST_NONE 0
# define ST_SIMPLE 1
# define ST_MEDIUM 2
# define ST_COMPLEX 3
# define ST_ADAPTIVE 4

# include "libft/libft.h"

typedef struct s_stack
{
	int				content;
	int				index;
	char			indexed;
	void			*next;
	void			*prev;
}	t_stack;

typedef struct s_bench
{
	char	on;
	float	disorder;
	char	strategy;
	size_t	total;
	size_t	sa;
	size_t	sb;
	size_t	ss;
	size_t	pa;
	size_t	pb;
	size_t	ra;
	size_t	rb;
	size_t	rr;
	size_t	rra;
	size_t	rrb;
	size_t	rrr;
}	t_bench;

void	ps_radix(t_stack **stack_a, t_stack **stack_b, t_bench *bench);

int		check_params(int argn, char **argv, t_bench *bench);
int		ps_split(int arg, char **argv, t_stack **stack_a, t_bench *bench);
int		ps_atoi(const char *nptr, int *out);

/* push_swap_lst.c */
t_stack	*ps_lstnew(int content, t_stack *prev);
int		ps_disorder(t_stack *stack, t_bench *bench);
void	ps_debug_lst(t_stack *lst);

/* push_swap_utils.c */
int		ps_lst_len(t_stack *stack);
int		ps_dups(t_stack *stack);

/* push_swap_algorithms.c */
void	ps_calc_min(t_stack *stack, int *min_pos, int *min_val);
int		ps_bench_and_simple(t_stack **stack_a, t_stack **stack_b, t_bench *b);
int		ps_do_simple(t_stack **stack_a, t_stack **stack_b, t_bench *bench);
int		ps_do_five(t_stack **stack_a, t_bench *bench);

/* push_swap_movement.c */
int		ps_sx(t_stack **statck, char ab, t_bench *bench);
int		ps_ss(t_stack **statck_a, t_stack **statck_b, t_bench *bench);
int		ps_rx(t_stack **stack, char ab, t_bench *bench);
int		ps_rr(t_stack **stack_a, t_stack **stack_b, t_bench *bench);
int		ps_rrx(t_stack **stack, char ab, t_bench *bench);
int		ps_rrr(t_stack **stack_a, t_stack **stack_b, t_bench *bench);
int		ps_px(t_stack **stack_a, t_stack **stack_b, t_bench *bench, char ab);
int		ps_adaptive(t_stack **stack_a, t_stack **stack_b, t_bench *bench);
void	ps_bench_start(t_bench *bench);
void	ps_bench_total(t_bench *bench);
void	ps_bench_movements(t_bench *bench);
void	ps_bench_strategy(t_bench *bench, int selected);

/* push_swap_medium.c */
int		ps_bucket(t_stack **stack_a, t_stack **stack_b, t_bench *bench);

void	create_index(t_stack *stack, int len);

#endif
