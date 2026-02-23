/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_str_is_numeric.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/12 12:32:31 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/12 15:12:44 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

int	ft_str_is_numeric(char *str)
{
	while (*str != '\0')
	{
		if (!(*str >= '0' && *str <= '9' ))
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

	c = '0' + ft_str_is_numeric("12343142");
	write (1, &c, 1);

	c = '0' + ft_str_is_numeric("1234r4");
	write (1, &c, 1);


	c = '0' + ft_str_is_numeric("");
	write (1, &c, 1);
	return (0);
}*/
