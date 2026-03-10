/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap_movement_swap.c                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/23 17:50:17 by cmelero-          #+#    #+#             */
/*   Updated: 2026/01/30 17:32:45 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	ps_swap(t_stack **stack)
{
	t_stack	*nodo0;	
	t_stack	*nodo1;
	t_stack	*nodo2;
	t_stack	*nodo3;

	if (!*stack)
		return (1);
	if ((*stack)->next)
	{
		nodo0 = (*stack)->prev;
		nodo1 = *stack;
		nodo2 = nodo1->next;
		nodo3 = nodo2->next;
		nodo0->next = nodo2;
		nodo2->prev = nodo0;
		nodo1->next = nodo3;
		nodo2->next = nodo1;
		nodo1->prev = nodo2;
		nodo3->prev = nodo1;
		*stack = nodo2;
	}
	return (1);
}

int	ps_sx(t_stack **statck, char ab, t_bench *bench)
{
	ps_swap (statck);
	ft_printf ("s%c\n", ab);
	if (ab == 'a')
		bench->sa++;
	else
		bench->sb++;
	return (1);
}

int	ps_ss(t_stack **statck_a, t_stack **statck_b, t_bench *bench)
{
	ps_swap(statck_a);
	ps_swap(statck_b);
	ft_printf("ss\n");
	bench->ss++;
	return (1);
}

// rb - ra
int	ps_rx(t_stack **stack, char ab, t_bench *bench)
{
	if (*stack)
		*stack = (*stack)->next;
	ft_printf ("r%c\n", ab);
	if (ab == 'a')
		bench->ra++;
	else
		bench->rb++;
	return (1);
}

int	ps_rrr(t_stack **stack_a, t_stack **stack_b, t_bench *bench)
{
	if (*stack_a)
		*stack_a = (*stack_a)->prev;
	if (*stack_b)
		*stack_b = (*stack_b)->prev;
	ft_printf ("rrr\n");
	bench->rrr++;
	return (1);
}
