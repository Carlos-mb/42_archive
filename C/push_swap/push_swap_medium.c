/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap_medium.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/03 16:31:11 by catencio          #+#    #+#             */
/*   Updated: 2026/02/06 18:47:01 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	ps_sqrt(int n)
{
	int	i;

	i = 1;
	while ((i * i) <= n)
		i++;
	return (i - 1);
}

static int	max_index(t_stack *stack)
{
	int		max;
	t_stack	*start;

	max = stack->index;
	start = stack;
	while (stack->next != start)
	{
		stack = stack->next;
		if (stack->index > max)
			max = stack->index;
	}
	return (max);
}

static void	back_to_a(t_stack **stack_a, t_stack **stack_b, t_bench *bench)
{
	t_stack	*tmp;
	int		max_val;
	int		pos;
	int		len;

	len = ps_lst_len(*stack_b);
	max_val = max_index(*stack_b);
	tmp = *stack_b;
	pos = 0;
	while (tmp->index != max_val && ++pos)
		tmp = tmp->next;
	if (pos <= len / 2)
	{
		while ((*stack_b)->index != max_val)
			ps_rx(stack_b, 'b', bench);
	}
	else
	{
		while ((*stack_b)->index != max_val)
			ps_rrx(stack_b, 'b', bench);
	}
	ps_px(stack_a, stack_b, bench, 'a');
}

static void	distribute_buckets(t_stack **stack_a, t_stack **stack_b,
	t_bench *bench, int n)
{
	int	pushed;
	int	limit;
	int	sqrt_n;

	sqrt_n = ps_sqrt(n);
	limit = (n / sqrt_n);
	pushed = 0;
	while (pushed < n)
	{
		if (pushed >= limit && limit < n)
			limit = limit + (n / sqrt_n);
		if (pushed >= (n - (n % sqrt_n)))
			limit = n;
		if ((*stack_a)->index <= limit && ++pushed)
		{
			ps_px(stack_a, stack_b, bench, 'b');
			if ((*stack_b)->index <= (limit - ((n / sqrt_n) / 2)))
				ps_rx(stack_b, 'b', bench);
		}
		else
			ps_rx(stack_a, 'a', bench);
	}
}

int	ps_bucket(t_stack **stack_a, t_stack **stack_b, t_bench *bench)
{
	int	n;

	n = ps_lst_len(*stack_a);
	ps_bench_start(bench);
	ps_bench_strategy(bench, ST_MEDIUM);
	if (n < 10
		&& (bench->strategy == ST_ADAPTIVE || bench->strategy == ST_NONE))
	{
		ps_do_simple(stack_a, stack_b, bench);
		return (1);
	}
	create_index(*stack_a, n);
	distribute_buckets(stack_a, stack_b, bench, n);
	while (*stack_b)
		back_to_a(stack_a, stack_b, bench);
	return (1);
}
