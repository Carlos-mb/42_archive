/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_str_is_lowercase.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/12 12:32:31 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/12 15:13:47 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

int	ft_str_is_lowercase(char *str)
{
	while (*str != '\0')
	{
		if (!(*str >= 'a' && *str <= 'z' ))
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

	c = '0' + ft_str_is_lowercase("asdasda");
	write (1, &c, 1);

	c = '0' + ft_str_is_lowercase("4das");
	write (1, &c, 1);


	c = '0' + ft_str_is_lowercase("");
	write (1, &c, 1);
	return (0);
}*/
