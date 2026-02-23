/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap_adaptive.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/29 08:07:49 by cmelero-          #+#    #+#             */
/*   Updated: 2026/02/06 18:23:59 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	ps_adaptive(t_stack **stack_a, t_stack **stack_b, t_bench *bench)
{
	if (bench->disorder < 0.2)
		ps_bench_and_simple(stack_a, stack_b, bench);
	else if (bench->disorder < 0.5)
		ps_bucket(stack_a, stack_b, bench);
	else
		ps_radix(stack_a, stack_b, bench);
	return (1);
}
