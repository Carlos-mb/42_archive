/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_div_mod.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/11 10:40:49 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/11 10:50:05 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	ft_div_mod(int a, int b, int *div, int *mod)
{
	*div = a / b;
	*mod = a % b;
	return ;
}
/*
int main (void)
{
	char c;
	int div;
	int mod;

	ft_div_mod(6, 4, &div, &mod);

	c = div + '0';
	write (1,&c,1);
	c = mod + '0';
	write (1,&c,1);


	return (0);
}*/
