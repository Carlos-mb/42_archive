/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_iterative_factorial.c                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/20 13:43:24 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/24 12:30:15 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_iterative_factorial(int nb)
{
	int	salida;

	salida = 0;
	if (nb >= 0)
	{
		salida = 1;
		while (nb > 1)
			salida = salida * nb--;
	}
	return (salida);
}
/*
#include <stdio.h>

int main ()
{
	printf("%i", ft_iterative_factorial (-1));
}*/
