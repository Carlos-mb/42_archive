/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_sqrt.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/25 15:15:13 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/25 15:37:17 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_sqrt(int nb)
{
	int	i;

	i = 1;
	while ((i * i) <= nb)
	{
		if ((i * i) == nb)
			return (i);
		i++;
	}
	return (0);
}
/*
#include <stdio.h>
int main (void)
{
	printf("9:%i\n", ft_sqrt (9));
	printf("19:%i\n", ft_sqrt (19));
	printf("90:%i\n", ft_sqrt (90));
	printf("0:%i\n", ft_sqrt (0));
	printf("-9:%i\n", ft_sqrt (-9));
	printf("144:%i\n", ft_sqrt (144));
	printf("196:%i\n", ft_sqrt (196));
}*/
