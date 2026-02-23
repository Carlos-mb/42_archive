/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/18 10:55:09 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/21 14:29:48 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include <unistd.h>

void	ft_putnbr(int nb)
{
	char	c;

	if (nb == -2147483648)
		write (1, "-2147483648", 11);
	else if (nb == 0)
		write (1, "0", 1);
	else
	{
		if (nb < 1)
		{
			write (1, "-", 1);
			nb = nb *(-1);
		}
		if (nb > 9)
			ft_putnbr (nb / 10);
		c = '0' + (nb % 10);
		write (1, &c, 1);
	}
	return ;
}
/*
#include <stdio.h>

int main (void)
{

	ft_putnbr(0);
	write (1, "\n", 1);
	
	ft_putnbr(50);
	write (1, "\n", 1);
	
	ft_putnbr(51);
	write (1, "\n", 1);
	
	ft_putnbr(-59);
	write (1, "\n", 1);	
	
	ft_putnbr(-31415);
	write (1, "\n", 1);	

	ft_putnbr(31415);
	write (1, "\n", 1);	

	
	ft_putnbr(-2147483648);
	write (1, "\n", 1); 
	return (0);
}*/
