/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion_generic.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/05 14:19:52 by cmelero-          #+#    #+#             */
/*   Updated: 2026/05/05 14:23:37 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	ft_strcmp(char *s1, char *s2)
{
	int	i;

	i = 0;
	while (s1[i] && s2[i] && s1[i] == s2[i])
		i++;
	return (s1[i] - s2[i]);
}

int	ft_is_number(char *str)
{
	int	i;

	if (!str || !str[0])
		return (0);
	i = 0;
	while (str[i])
	{
		if (str[i] < '0' || str[i] > '9')
			return (0);
		i++;
	}
	return (1);
}

int	ft_atoi_safe(char *str, int *result)
{
	long long	n;
	int			i;

	if (!ft_is_number(str))
		return (0);
	n = 0;
	i = 0;
	while (str[i] && n <= 2147483647)
	{
		n = (n * 10) + (str[i] - '0');
		i++;
	}
	if (n > 2147483647)
		return (0);
	*result = (int)n;
	return (1);
}
