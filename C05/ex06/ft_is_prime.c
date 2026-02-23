/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_is_prime.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/25 15:22:28 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/25 15:59:40 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_is_prime(int nb)
{
	int	i;

	if (nb == 1)
		return (0);
	i = 2;
	while (i <= nb && (nb % i != 0))
	{
		i++;
	}
	if (nb % i == 0 && i == nb)
		return (1);
	return (0);
}

/*
#include <stdio.h>

int main(void)
{
	int i;

	i = 1;
	printf("%i:%i\n", i, ft_is_prime(i));
	i = 7;
	printf("%i:%i\n", i, ft_is_prime(i));
	i = 13;
	printf("%i:%i\n", i, ft_is_prime(i));
	i = 2;
	printf("%i:%i\n", i, ft_is_prime(i));
	i = 157;
	printf("%i:%i\n", i, ft_is_prime(i));
	i = 24649;
	printf("%i:%i\n", i, ft_is_prime(i));
}*/
