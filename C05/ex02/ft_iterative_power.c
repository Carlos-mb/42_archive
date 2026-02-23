/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_iterative_power.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/20 13:44:23 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/24 13:22:33 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_iterative_power(int nb, int power)
{
	int	salida;

	if (power < 0)
		salida = 0;
	else if (power == 0)
		salida = 1;
	else
	{
		salida = nb;
		while (power-- > 1)
			salida = nb * salida;
	}
	return (salida);
}
/*
#include <stdio.h>

int main ()
{
	printf("%i\n", ft_iterative_power (3, 3));
    printf("%i\n", ft_iterative_power (0, 0));
    printf("%i\n", ft_iterative_power (0, 1));
    printf("%i\n", ft_iterative_power (4, 4));
    printf("%i\n", ft_iterative_power (1, 1));
    printf("%i\n", ft_iterative_power (10, 0));
}*/
