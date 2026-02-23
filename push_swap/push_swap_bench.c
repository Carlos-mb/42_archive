/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap_bench.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/30 13:23:34 by cmelero-          #+#    #+#             */
/*   Updated: 2026/02/07 11:00:18 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	werr(char *s1, char pos, char to_free)
{
	if (pos == 1)
		write(2, "[bench] ", 8);
	write(2, s1, ft_strlen(s1));
	if (pos == 3)
		write(2, "\n", 1);
	if (to_free)
		free(s1);
}

void	ps_bench_start(t_bench *bench)
{
	if (bench->on)
	{
		werr("disorder: ", 1, 0);
		werr(ft_itoa((int)(bench->disorder * 100.00)), 2, 1);
		werr(".", 2, 0);
		werr(ft_itoa(
				100.00 * (bench->disorder - (int)(bench->disorder))), 2, 1);
		werr("%", 3, 0);
	}
}

void	ps_bench_strategy(t_bench *bench, int selected)
{
	if (bench->on)
	{
		werr("strategy: ", 1, 0);
		if (bench->strategy == ST_ADAPTIVE || bench->strategy == ST_NONE)
			werr("Adapive / ", 2, 0);
		if (selected == ST_SIMPLE)
			werr("Simple  (O(n2))", 3, 0);
		else if (selected == ST_COMPLEX)
			werr("Complex O(n log n)", 3, 0);
		else if (selected == ST_MEDIUM)
			werr("Medium O(n√n)", 3, 0);
	}
}

void	ps_bench_total(t_bench *bench)
{
	bench->total = bench->sa;
	bench->total += bench->sb;
	bench->total += bench->ss;
	bench->total += bench->pa;
	bench->total += bench->pb;
	bench->total += bench->ra;
	bench->total += bench->rb;
	bench->total += bench->rr;
	bench->total += bench->rra;
	bench->total += bench->rrb;
	bench->total += bench->rrr;
	if (bench->on)
	{
		werr("total_ops: ", 1, 0);
		werr(ft_itoa(bench->total), 3, 1);
	}
}

void	ps_bench_movements(t_bench *bench)
{
	if (bench->on)
	{
		werr("sa: ", 1, 0);
		werr(ft_itoa(bench->sa), 2, 1);
		werr(" sb: ", 2, 0);
		werr(ft_itoa(bench->sb), 2, 1);
		werr(" ss: ", 2, 0);
		werr(ft_itoa(bench->ss), 2, 1);
		werr(" pa: ", 2, 0);
		werr(ft_itoa(bench->pa), 2, 1);
		werr(" pb: ", 2, 0);
		werr(ft_itoa(bench->pb), 3, 1);
		werr("ra: ", 1, 0);
		werr(ft_itoa(bench->ra), 2, 1);
		werr(" rb: ", 2, 0);
		werr(ft_itoa(bench->rb), 2, 1);
		werr(" rb: ", 2, 0);
		werr(ft_itoa(bench->rr), 2, 1);
		werr(" rra: ", 2, 0);
		werr(ft_itoa(bench->rra), 2, 1);
		werr(" rrb: ", 2, 0);
		werr(ft_itoa(bench->rrb), 2, 1);
		werr(" rrr: ", 2, 0);
		werr(ft_itoa(bench->rrr), 3, 1);
	}
}
