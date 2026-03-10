/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap_more_utils.c                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/07 10:17:43 by cmelero-          #+#    #+#             */
/*   Updated: 2026/02/07 10:23:32 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	ps_disorder(t_stack *stack, t_bench *bench)
{
	int		mistakes;
	int		total_pairs;
	t_stack	*to_loop;
	t_stack	*start_stack;	

	bench->disorder = 0;
	if (stack && stack != stack->next)
	{
		mistakes = 0;
		total_pairs = 0;
		start_stack = stack;
		while (stack->next != start_stack)
		{
			to_loop = stack->next;
			while (to_loop->next != start_stack->next)
			{
				total_pairs++;
				mistakes += (stack->content > to_loop->content);
				to_loop = to_loop->next;
			}
			stack = stack->next;
		}
		bench->disorder = (float)mistakes / total_pairs;
	}
	return (bench->disorder);
}

void	create_index(t_stack *stack, int len)
{
	t_stack	*current_min_node;
	t_stack	*start;
	int		cur_index;

	cur_index = -1;
	current_min_node = stack;
	start = stack;
	while (cur_index < len - 1)
	{
		while (1)
		{
			if (stack->index < current_min_node->index && !(stack->indexed))
				current_min_node = stack;
			stack = stack->next;
			if (stack == start)
				break ;
		}
		current_min_node->index = ++cur_index;
		current_min_node->indexed = 1;
		stack = start;
		current_min_node = start;
		while (cur_index < len -1 && current_min_node->indexed)
			current_min_node = current_min_node->next;
	}
}
