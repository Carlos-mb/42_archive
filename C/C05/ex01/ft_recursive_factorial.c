/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_recursive_factorial.c                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/20 13:43:54 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/24 12:33:02 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_recursive_factorial(int nb)
{
	int	salida;

	salida = 0;
	if (nb > 1)
		salida = nb * ft_recursive_factorial (nb - 1);
	else if (nb == 1 || nb == 0)
		salida = 1;
	return (salida);
}
/*
#include <stdio.h>
int main ()
{
	printf("%i", ft_recursive_factorial (3));
	return (0);
}*/
