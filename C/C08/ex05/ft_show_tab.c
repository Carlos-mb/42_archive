/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_show_tab.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/27 08:30:31 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/27 12:58:06 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <unistd.h>
#include "ft_stock_str.h"

void	ft_putnum(int i)
{
	char	c;

	if (i > 9)
		ft_putnum (i / 10);
	i = i % 10;
	c = '0' + (i);
	write (1, &c, 1);
	return ;
}

void	ft_putstr(char *str)
{
	int		i;
	char	c;

	i = 0;
	while (str[i])
	{
		c = str[i++];
		write(1, &c, 1);
	}
	write(1, "\n", 1);
}

void	ft_show_tab(struct s_stock_str *par)
{
	int	i;

	i = 0;
	while (par[i].str != NULL)
	{
		ft_putstr(par[i].str);
		ft_putnum(par[i].size);
		write(1, "\n", 1);
		ft_putstr(par[i].copy);
		i++;
	}
}
/*

struct s_stock_str *ft_strs_to_tab(int ac, char **av);
int main (void)
{
	char *textos[4] = {"Carlkjlfgkjldfkjldfgkljdfkjldfkjldfkljfklfgklfgkljfklsjfdgkljfdjkldfskldjsfgdsgkljdfkljdfkljfdgdklfjdkljfgdfkljdfkgjkldgkljdlkjdflkjdfjkldfsjkldfgdgdkljflkjdfgjkldflkjlkjflkdlkjdfskljdgffskljdgfklsgfkljgskljfdos", "Melero", "Nadando", "Ando"};
	t_stock_str *result = ft_strs_to_tab(4,textos);

	ft_show_tab(result);
	
	return (0);
}*/
