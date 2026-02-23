/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_ultimate_div_mod.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/11 10:51:22 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/11 10:58:45 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	ft_ultimate_div_mod(int *a, int *b)
{
	int	div;
	int	mod;

	div = *a / *b;
	mod = *a % *b;
	*a = div;
	*b = mod;
	return ;
}
/*
int main(void)

{
	int a = 6;
	int b = 4;
	char c ;

	ft_ultimate_div_mod (&a, &b);

	c = a +'0';
	write (1,&c,1);
	c = b + '0';
	write (1, &c,1);



	return (0) ;
}*/
