/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_str_is_uppercase.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/12 12:32:31 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/12 15:15:04 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

int	ft_str_is_uppercase(char *str)
{
	while (*str != '\0')
	{
		if (!(*str >= 'A' && *str <= 'Z' ))
		{
			return (0);
		}
		str++;
	}
	return (1);
}
/*
int	main(void)
{
	char c;

	c = '0' + ft_str_is_uppercase("ASD");
	write (1, &c, 1);

	c = '0' + ft_str_is_uppercase("A4");
	write (1, &c, 1);


	c = '0' + ft_str_is_uppercase("");
	write (1, &c, 1);
	return (0);
}*/
