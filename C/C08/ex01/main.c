/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/26 09:29:54 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/26 10:27:15 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "./ft_boolean.h"
void ft_putstr(char *str)
{
	while (*str)
	write(1, str++, 1);
}
t_bool ft_is_even(int nbr)
{
	return ((EVEN(nbr)) ? TRUE : FALSE);
}
int main(int argc, char **argv)
{
	(void)argv;
	if (ft_is_even(argc - 1) == TRUE)
		ft_putstr(EVEN_MSG);
	else
		ft_putstr(ODD_MSG);
	return (SUCCESS);
}
