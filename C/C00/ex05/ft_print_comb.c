/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_comb.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/10 10:17:20 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/10 12:47:52 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include <stdio.h> // BORRAAMEEEEE

void	ft_print_comb(void);

int	main(void)

{
	ft_print_comb();
}

void	write2(int a, int b, int c)
{
	int	ch;

	ch = a + '0';
	write (1, &ch, 1);
	ch = b + '0';
	write (1, &ch, 1);
	ch = c + '0';
	write (1, &ch, 1);
	if ((a * 100 + b * 10 + c) != 789)
	{
		write (1, ", ", 2);
	}
}

void	ft_print_comb(void)
{
	int	a;
	int	b;
	int	c;

	a = 0;
	while (a <= 7)
	{
		b = a + 1;
		while (b <= 8)
		{
			c = b + 1;
			while (c <= 9)
			{
				write2(a, b, c);
				c++;
			}
			b++;
		}
		a++;
	}
	return ;
}
