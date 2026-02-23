/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_sort_int_tab.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/11 11:58:50 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/11 13:08:07 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//#include <stdio.h>
#include <unistd.h>

int	ft_sort_int_tab2(int *tab, int size);

void	ft_sort_int_tab(int *tab, int size)
{
	while (ft_sort_int_tab2(tab, size) != 0)
	{
	}
	return ;
}

int	ft_sort_int_tab2(int *tab, int size)
{
	int	i;
	int	changed;
	int	tmp;

	changed = 0;
	i = 1;
	while (i < size)
	{
		if (tab[i] > tab[i - 1])
		{
			tmp = tab [i];
			tab [i] = tab [i - 1];
			tab [i - 1] = tmp;
			changed = 1;
		}
		i++;
	}
	return (changed);
}
/*
int main(void)
{
	int tab[4]={1,2,3,4};

	ft_sort_int_tab(tab, 4);


	printf("saldia: %i%i%i%i", tab[0], tab[1], tab[2], tab[3]);		

}*/
