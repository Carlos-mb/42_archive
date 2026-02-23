/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_fibonacci.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/20 13:46:00 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/22 10:43:39 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_fibonacci(int index)
{
	int	salida;

	if (index < 0)
		salida = -1;
	else if (index == 0 || index == 1)
		salida = index;
	else
		salida = ft_fibonacci(index - 1) + ft_fibonacci(index - 2);
	return (salida);
}
/*
#include <stdio.h>
int main (void)
{
	printf("%i\n",ft_fibonacci(0));
    printf("%i\n",ft_fibonacci(1));
    printf("%i\n",ft_fibonacci(2));
    printf("%i\n",ft_fibonacci(3));
    printf("%i\n",ft_fibonacci(4));
   	printf("%i\n",ft_fibonacci(5));    
    printf("%i\n",ft_fibonacci(16));
    
	return (0);
}*/
