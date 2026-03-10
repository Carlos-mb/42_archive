/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap_radix.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/27 12:36:42 by cmelero-          #+#    #+#             */
/*   Updated: 2026/02/07 10:23:27 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	ps_digit(int pos, int number)
{
	int	j;

	j = 10;
	while (--pos)
		j = j * 10;
	return ((number - ((number / j) * j)) / (j / 10));
}

int	will_i_find(int digit, t_stack *stack, int i)
{
	t_stack	*to_move;

	if (!stack)
		return (0);
	to_move = stack;
	while (1)
	{
		if (ps_digit(digit, to_move->index) == i)
			return (1);
		to_move = to_move->next;
		if (stack == to_move)
			break ;
	}
	return (0);
}

static void	move_block(int digit, t_stack **stack_a,
	t_stack **stack_b, t_bench *bench)
{
	int		i;
	int		cont;

	i = 0;
	while (i <= 9)
	{
		cont = ps_lst_len(*stack_a);
		if (will_i_find(digit, *stack_a, i))
		{
			while (cont--)
			{
				if (ps_digit(digit, (*stack_a)->index) == i)
					ps_px(stack_a, stack_b, bench, 'b');
				else
					ps_rx(stack_a, 'a', bench);
			}
		}
		i++;
	}
}

static void	reverse_block(int digit, t_stack **stack_a,
	t_stack **stack_b, t_bench *bench)
{
	int		i;
	int		cont;

	i = 9;
	while (i >= 0)
	{
		cont = ps_lst_len(*stack_b);
		if (will_i_find(digit, *stack_b, i))
		{
			while (cont--)
			{
				if (ps_digit(digit, (*stack_b)->index) == i)
					ps_px(stack_a, stack_b, bench, 'a');
				else
					ps_rx(stack_b, 'b', bench);
			}
		}
		i--;
	}
}

void	ps_radix(t_stack **stack_a, t_stack **stack_b, t_bench *bench)
{
	int		digit;
	int		len;

	ps_bench_start(bench);
	ps_bench_strategy(bench, ST_COMPLEX);
	len = ft_digits(ps_lst_len(*stack_a));
	if (len == 1
		&& (bench->strategy == ST_ADAPTIVE || bench->strategy == ST_NONE))
	{
		ps_do_simple(stack_a, stack_b, bench);
		return ;
	}
	create_index(*stack_a, ps_lst_len(*stack_a));
	digit = 1;
	while (digit <= len)
	{
		if (digit % 2 != 0)
			move_block(digit, stack_a, stack_b, bench);
		else
			reverse_block(digit, stack_a, stack_b, bench);
		digit++;
	}
	while (*stack_b)
		ps_px(stack_a, stack_b, bench, 'a');
}
