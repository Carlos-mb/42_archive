/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap_simple.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/24 17:53:42 by cmelero-          #+#    #+#             */
/*   Updated: 2026/02/07 23:43:07 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	ps_calc_min(t_stack *stack, int *min_pos, int *min_val)
{
	int		i;
	t_stack	*start;

	start = stack;
	i = 1;
	while (1)
	{
		if (*min_val > stack->content)
		{
			*min_val = stack->content;
			*min_pos = i;
		}
		stack = stack->next;
		if (stack == start)
			break ;
		else
			i++;
	}
}

static void	ps_move(int min_pos, int len, t_stack **stack_a, t_bench *ben)
{
	if (1 || min_pos <= ((len + 1) / 2))
		while (min_pos-- != 1)
			ps_rx(stack_a, 'a', ben);
	else
		while (min_pos++ <= len)
			ps_rrx(stack_a, 'a', ben);
}

static int	ps_do_three(t_stack **stack_a, t_bench *bench)
{
	int	first;
	int	second;
	int	third;

	first = (*stack_a)->content;
	second = ((t_stack *)((*stack_a)->next))->content;
	third = ((t_stack *)((*stack_a)->prev))->content;
	if (first > second && first > third && second > third)
	{
		ps_rx(stack_a, 'a', bench);
		ps_sx(stack_a, 'a', bench);
	}
	else if (first > second && first > third && second < third)
		ps_rx(stack_a, 'a', bench);
	else if (first > second)
		ps_sx(stack_a, 'a', bench);
	else if (first > third)
		ps_rrx(stack_a, 'a', bench);
	else
	{
		ps_sx(stack_a, 'a', bench);
		ps_rx(stack_a, 'a', bench);
	}
	return (1);
}

int	ps_do_simple(t_stack **stack_a, t_stack **stack_b, t_bench *bench)
{
	int	min_val;
	int	min_pos;
	int	len;

	if (!*stack_a || (*stack_a)->next == *stack_a || bench->disorder == 0)
		return (1);
	if (ps_lst_len(*stack_a) == 3)
		ps_do_three(stack_a, bench);
	while ((*stack_a)->next != *stack_a)
	{
		min_val = (*stack_a)->content;
		min_pos = 1;
		ps_calc_min(*stack_a, &min_pos, &min_val);
		len = ps_lst_len(*stack_a);
		if (min_pos != 1)
			ps_move(min_pos, len, stack_a, bench);
		if (len == 2)
			break ;
		ps_px(stack_a, stack_b, bench, 'b');
	}
	while (*stack_b)
		ps_px(stack_a, stack_b, bench, 'a');
	return (1);
}

int	ps_bench_and_simple(t_stack **stack_a, t_stack **stack_b,	t_bench *bench)
{
	ps_bench_start(bench);
	ps_bench_strategy(bench, ST_SIMPLE);
	return (ps_do_simple(stack_a, stack_b, bench));
}
