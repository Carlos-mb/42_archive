/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap_movement_push.c                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/29 12:50:17 by cmelero-          #+#    #+#             */
/*   Updated: 2026/02/06 08:18:01 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	ps_push(t_stack **stack_1, t_stack **stack_2)
{
	t_stack	*nodo10;	
	t_stack	*nodo11;
	t_stack	*nodo12;

	if (!*stack_1)
		return (0);
	nodo11 = *stack_1;
	nodo10 = nodo11->prev;
	nodo12 = nodo11->next;
	nodo10->next = nodo12;
	nodo12->prev = nodo10;
	nodo11->prev = nodo11;
	nodo11->next = nodo11;
	*stack_1 = nodo12;
	if (*stack_2)
	{
		nodo11->next = *stack_2;
		nodo11->prev = (*stack_2)->prev;
		((t_stack *)(*stack_2)->prev)->next = nodo11;
		(*stack_2)->prev = nodo11;
	}
	*stack_2 = nodo11;
	if (*stack_1 == *stack_2)
		*stack_1 = NULL;
	return (1);
}

int	ps_rr(t_stack **stack_a, t_stack **stack_b, t_bench *bench)
{
	if (*stack_a)
		*stack_a = (*stack_a)->next;
	if (*stack_b)
		*stack_b = (*stack_b)->next;
	ft_printf ("rr\n");
	bench->rr++;
	return (1);
}

// rrb - rra
int	ps_rrx(t_stack **stack, char ab, t_bench *bench)
{
	if (*stack)
		*stack = (*stack)->prev;
	ft_printf ("rr%c\n", ab);
	if (ab == 'a')
		bench->rra++;
	else
		bench->rrb++;
	return (1);
}

int	ps_px(t_stack **stack_a, t_stack **stack_b, t_bench *bench, char ab)
{
	if (ab == 'a')
	{
		ps_push(stack_b, stack_a);
		ft_printf ("pa\n");
		bench->pa++;
	}
	else
	{
		ps_push(stack_a, stack_b);
		ft_printf("pb\n");
		bench->pb++;
	}
	return (1);
}
