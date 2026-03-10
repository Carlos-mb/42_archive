/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_swap.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/11 10:27:26 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/11 10:39:58 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	ft_swap(int *a, int *b)
{
	int	tmp;

	tmp = *a;
	*a = *b;
	*b = tmp;
	return ;
}
/*


int main (void)
{
	int a=1;
	int b=2;	
	char c;

	c = a + '0';
	write(1, &c, 1);
	c = b + '0';
	write(1, &c, 1);

	ft_swap (&a, &b);

	c = a + '0';
	write (1, &c, 1);
	c = b + '0';
	write (1, &c, 1);

	return(0);
}*/
