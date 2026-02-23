/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_recursive_power.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/20 13:44:51 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/24 13:24:13 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_recursive_power(int nb, int power)
{
	int	salida;

	if (power < 0)
		salida = 0;
	else if (power == 0)
		salida = 1;
	else
	{
		salida = nb * ft_recursive_power (nb, power - 1);
	}
	return (salida);
}
/*
#include <stdio.h>

int main ()
{
printf("%i\n",  ft_recursive_power (3, 3));
printf("%i\n",  ft_recursive_power (0, 0));
    printf("%i\n",  ft_recursive_power (0, 1));
    printf("%i\n",  ft_recursive_power (4, 4));
    printf("%i\n",  ft_recursive_power (1, 1));
    printf("%i\n",  ft_recursive_power (10, 0));
}
*/
