/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr_base.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/19 10:45:12 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/21 14:31:09 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

int	noterr(char *base)
{
	int	salida;
	int	len;
	int	i;
	int	j;

	salida = 0;
	len = 0;
	i = 0;
	while (base[i] != '\0' && salida == 0)
	{
		if (base [i] == '-' || base [i] == '+' || base [i] == ' ')
			salida = 1;
		j = i + 1;
		while (base[j] && salida == 0)
		{
			if (base[i] == base[j])
				salida = 1;
			j++;
		}
		len++;
		i++;
	}
	if (len < 1)
		salida = 1;
	return (salida);
}

void	ft_add_char(int resto, char *base, char *result)
{
	int		i;
	char	c;

	i = 0;
	while (result [i] != '\0')
		i++;
	c = i + '0';
	while (i >= 0)
	{
		result[i + 1] = result [i];
		c = i + '0';
		i--;
	}
	result [0] = base[resto];
	return ;
}

void	doit(int nbr, char *base, char *result, int size)
{
	int	resto;

	resto = nbr % size;
	ft_add_char(resto, base, result);
	if ((nbr / size) != 0)
	{
		doit(nbr / size, base, result, size);
	}
	return ;
}

void	printit(char *result, int negativo)
{
	int	i;

	if (negativo == 1)
		write (1, "-", 1);
	i = 0;
	while (result[i] != '\0')
	{
		write (1, &result[i++], 1);
	}
}

void	ft_putnbr_base(int nbr, char *base)
{
	int		i;
	char	result[100];
	int		negativo;

	i = noterr(base);
	negativo = 0;
	if (i == 0)
	{
		i = 0;
		result [0] = '\0';
		while (base[i] != '\0')
		{
			i++;
		}
		if (nbr < 0)
		{
			nbr = -nbr;
			negativo = 1;
		}
		doit(nbr, base, result, i);
		printit (result, negativo);
	}
	return ;
}

/*	
#include <stdlib.h>
#include <stdio.h>

int main ()
{
	ft_putnbr_base (1, "01"); // 1
	write (1, "\n*****\n", 7);
	ft_putnbr_base (-15, "01"); // 1111 (4)
	write (1, "\n*****\n", 7);
	ft_putnbr_base (16, "01"); // 10000 
	write (1, "\n*****\n", 7);
	ft_putnbr_base (80,   "0123456789ABCDEF"); // 50
	write (1, "\n*****\n", 7);
	ft_putnbr_base (16,  "0123456789ABCDEF"); // 10
	write (1, "\n*****\n", 7);
	ft_putnbr_base (300, "0123456789ABCDEF"); // 12C
	write (1, "\n*****\n", 7);
	ft_putnbr_base (0, "poniguay"); // p
	write (1, "\n*****\n", 7);
	ft_putnbr_base (1, "poniguay"); // o
	write (1, "\n*****\n", 7);
	ft_putnbr_base (2, "poniguay"); //n
	write (1, "\n*****\n", 7);
	ft_putnbr_base (-2, "poniguay"); //n	
	write (1, "\n*****\n", 7);
	ft_putnbr_base (1923, "caso"); // aoscco
	write (1, "\nNADAS\n", 7);
//	write (1, "\n1****\n", 7);
	ft_putnbr_base (1923, ""); 
//	write (1, "\n2****\n", 7);
	ft_putnbr_base (1923, " ");
//	write (1, "\n3****\n", 7);
	ft_putnbr_base (1923, "casoa");
//	write (1, "\n4****\n", 7);
	ft_putnbr_base (1923, "ca-so");	
	
	
	
			
// 	ft_putnbr_base (atoi(argv[1]), argv[2]);
	
}*/
