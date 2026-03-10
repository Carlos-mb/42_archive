/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_rev_int_tab.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/11 11:58:50 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/11 12:45:05 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//#include <stdio.h>
#include <unistd.h>

void	ft_rev_int_tab(int *tab, int size)
{
	int	i;
	int	tmp;

	i = 0;
	while (i < size / 2)
	{
		tmp = tab[i];
		tab[i] = tab [size - i - 1];
		tab[size - i - 1] = tmp;
		i++;
	}
}
/*
int main(void)
{
	int tab[5]={1,2,3,4,5};

	ft_rev_int_tab(tab, 5);


	printf("saldia: %i%i%i%i%i", tab[0], tab[1], tab[2], tab[3], tab[4]);		

}*/
