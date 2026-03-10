/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/21 09:48:09 by cmelero-          #+#    #+#             */
/*   Updated: 2026/02/06 18:55:22 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	ps_free_stack(t_stack *node)
{
	t_stack	*last;

	if (!node)
		return ;
	last = node->prev;
	while (node != last)
	{
		node = node->next;
		free((t_stack *)node->prev);
	}
	free(last);
}

static int	ps_init(int argn, char **argv, t_bench *bench, t_stack **stack_a)
{
	if (!(check_params(argn, argv, bench)
			&& ps_split(argn, argv, stack_a, bench)
			&& ps_dups(*stack_a)))
	{
		ft_printf("Error\n");
		ps_free_stack(*stack_a);
		free(bench);
		return (0);
	}
	return (1);
}

static void	doit(t_stack **stack_a, t_stack **stack_b, t_bench *bench)
{
	if (bench->disorder != 0)
	{
		if (bench->strategy == ST_SIMPLE)
			ps_bench_and_simple(stack_a, stack_b, bench);
		else if (bench->strategy == ST_COMPLEX)
			ps_radix(stack_a, stack_b, bench);
		else if (bench->strategy == ST_MEDIUM)
			ps_bucket(stack_a, stack_b, bench);
		else if (bench->strategy == ST_ADAPTIVE || bench->strategy == ST_NONE)
			ps_adaptive(stack_a, stack_b, bench);
	}
	else
		ps_bench_start(bench);
	ps_bench_total(bench);
	ps_bench_movements(bench);
}

static int	fill_bench(t_bench *bench)
{
	bench->on = 0;
	bench->disorder = 0;
	bench->strategy = ST_NONE;
	bench->total = 0;
	bench->sa = 0;
	bench->sb = 0;
	bench->ss = 0;
	bench->pa = 0;
	bench->pb = 0;
	bench->ra = 0;
	bench->rb = 0;
	bench->rr = 0;
	bench->rra = 0;
	bench->rrb = 0;
	bench->rrr = 0;
	return (1);
}

int	main(int argn, char **argv)
{
	t_stack	*stack_a;
	t_stack	*stack_b;
	t_bench	*bench;

	if (argn < 2)
		return (0);
	stack_a = NULL;
	stack_b = NULL;
	bench = malloc (sizeof(t_bench));
	if (!bench)
	{
		ft_printf("Error\n");
		return (0);
	}
	fill_bench(bench);
	if (!ps_init(argn, argv, bench, &stack_a))
		return (0);
	doit(&stack_a, &stack_b, bench);
	ps_free_stack(stack_a);
	ps_free_stack(stack_b);
	free(bench);
}
