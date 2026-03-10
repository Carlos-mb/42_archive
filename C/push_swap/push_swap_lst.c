/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap_lst.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/09 18:21:30 by cmelero-          #+#    #+#             */
/*   Updated: 2026/02/07 10:20:58 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_stack	*ps_lstnew(int content, t_stack *prev)
{
	t_stack	*output;

	output = malloc(sizeof(t_stack));
	if (!(output))
		return (NULL);
	output->content = content;
	output->index = content;
	output->indexed = 0;
	output->next = NULL;
	output->prev = prev;
	return (output);
}

/*
Adds a new node next to the one refered and change the pointer to the new one 
cur_node is NULL if the list does not exist
*/
int	additem(t_stack **stack_a, t_stack **cur_node, int content)
{
	t_stack	*new_node;

	new_node = ps_lstnew(content, NULL);
	if (!new_node)
		return (0);
	if (!*stack_a)
	{
		*stack_a = new_node;
		(*stack_a)->prev = new_node;
		(*stack_a)->next = new_node;
	}
	else
	{
		new_node->prev = *cur_node;
		new_node->next = *stack_a;
		(*stack_a)->prev = new_node;
		(*cur_node)->next = new_node;
	}
	*cur_node = new_node;
	return (1);
}

static int	ps_free_spt(char **spt)
{
	size_t	i;

	i = 0;
	while ((spt)[i])
	{
		free((spt)[i]);
		i++;
	}
	free(spt);
	return (1);
}

// Create lst from parameters
int	ps_split(int arg, char **argv, t_stack **stack_a, t_bench *bench)
{
	int		i;
	t_stack	*cur_node;
	int		val;
	char	**spt;
	ssize_t	j;

	val = 0;
	cur_node = NULL;
	i = bench->on + (bench->strategy != ST_NONE);
	while (++i < arg)
	{
		spt = ft_split(argv[i], ' ');
		j = -1;
		while (spt[++j])
		{
			if (!(ps_atoi(spt[j], &val) && additem(stack_a, &cur_node, val)))
			{
				ps_free_spt(spt);
				return (0);
			}
		}
		ps_free_spt(spt);
	}
	ps_disorder(*stack_a, bench);
	return (*stack_a != NULL);
}

int	ps_lst_len(t_stack *stack)
{
	int			i;
	t_stack		*start_stack;

	if (!stack)
		return (0);
	start_stack = stack;
	i = 1;
	while (stack->next != start_stack && i++)
		stack = stack->next;
	return (i);
}
