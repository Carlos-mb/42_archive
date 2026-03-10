/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strs_to_tab.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/27 07:33:35 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/27 09:40:20 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_stock_str.h"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int	ft_strlen(char *str)
{
	int	i;

	i = 0;
	while (str[i] != '\0')
		i++;
	return (i);
}

void	ft_strcopy(char *dest, char *ori)
{
	int	i;

	i = 0;
	while (ori[i] != '\0')
	{
		dest[i] = ori[i];
		i++;
	}
	dest[i] = '\0';
	return ;
}

struct	s_stock_str	*ft_strs_to_tab(int ac, char **av)
{
	t_stock_str	*result;
	int			i;

	result = malloc(sizeof(t_stock_str) * (ac + 1));
	if (result == NULL)
		return (NULL);
	i = -1;
	while (++i < ac)
	{
		result[i].size = ft_strlen(av[i]);
		result[i].str = av[i];
		result[i].copy = malloc((result[i].size + 1) * sizeof(char));
		if (result[i].copy == NULL)
		{
			while (i > 0)
				free(result[--i].copy);
			free(result);
			return (NULL);
		}
		ft_strcopy(result[i].copy, av[i]);
	}
	result[i].size = 0;
	result[i].copy = 0;
	result[i].str = 0;
	return (result);
}
/*
void ft_putnum (int i)
{
	char c;
	if (i > 9)
		ft_putnum (i / 10);
	i = i % 10;
	c = '0' + (i);
	write (1, &c, 1);
	write (1, "\n", 1);
	return ;
}

void ft_putstr(char *str)
{
	int i;
	char c;

	i=0;

	while (str[i])
	{
		c = str[i++];
		write(1, &c, 1);
	}
	write(1,"\n",1);
}

void ft_show_tab(struct s_stock_str *par)
{
	int	i;
	
	i = 0;
	while (par[i].str != NULL)
	{
		ft_putstr(par[i].str);
		ft_putnum(par[i].size);
		ft_putstr(par[i].copy);
		i++;
	}
}	
int main (void)
{
	char *textos[4] = {"Carlos", "Melero", "Nadando", "Ando"};
	t_stock_str *result = ft_strs_to_tab(4,textos);

	ft_show_tab(result);
	
	return (0);
}*/
