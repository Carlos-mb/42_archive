/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap_utils.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/21 09:55:26 by cmelero-          #+#    #+#             */
/*   Updated: 2026/02/07 10:24:05 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	ps_dups(t_stack *stack)
{
	t_stack	*to_loop;
	t_stack	*start_stack;	

	if (stack == stack->next)
		return (1);
	start_stack = stack;
	while (stack->next != start_stack)
	{
		to_loop = stack->next;
		while (to_loop->next != start_stack->next)
		{
			if (stack->content == to_loop->content)
				return (0);
			to_loop = to_loop->next;
		}
		stack = stack->next;
	}
	return (1);
}

static int	check_param(char *param, t_bench *bench)
{
	if (!ft_strncmp(param, "--", 2))
	{
		if (!ft_strncmp(param, "--bench", 8))
			bench->on = 1;
		else if (!ft_strncmp(param, "--simple", 9))
			bench->strategy = ST_SIMPLE;
		else if (!ft_strncmp(param, "--medium", 9))
			bench->strategy = ST_MEDIUM;
		else if (!ft_strncmp(param, "--complex", 10))
			bench->strategy = ST_COMPLEX;
		else if (!ft_strncmp(param, "--adaptive", 11))
			bench->strategy = ST_ADAPTIVE;
		else
			return (0);
	}
	return (1);
}

int	check_params(int argn, char **argv, t_bench *bench)
{
	bench->strategy = ST_NONE;
	bench->on = 0;
	if (argn > 1)
		if (!check_param(argv[1], bench))
			return (0);
	if (argn > 2)
		if (!check_param(argv[2], bench))
			return (0);
	return (1);
}

// Atoi with special error checks
int	ps_atoi(const char *nptr, int *out)
{
	long	i;
	int		sign;

	while (*nptr == ' ')
		nptr++;
	sign = 1 - (2 * (*nptr == '-'));
	nptr = nptr + (*nptr == '+' || *nptr == '-');
	i = 0;
	if (!(*nptr))
		return (0);
	while (*nptr)
	{
		if (*nptr >= '0' && *nptr <= '9')
			i = (i * 10) + (*nptr - '0');
		else
			return (0);
		nptr++;
	}
	i *= sign;
	if (i != (long)(int)i)
		return (0);
	*out = (int)i;
	return (1);
}
