/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_str_is_alpha.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/12 12:32:31 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/12 12:53:19 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

int	ft_str_is_alpha(char *str)
{
	while (*str != '\0')
	{
		if (!((*str >= 'a' && *str <= 'z' ) || (*str >= 'A' && *str <= 'Z')))
		{
			return (0);
		}
		str++;
	}
	return (1);
}
/*
int main(void)
{
	char c;

	c = '0' + ft_str_is_alpha("AAAAaaaa");
	write (1, &c, 1);

	c = '0' + ft_str_is_alpha("AAAA6aaaa");
	write (1, &c, 1);
	return (0);
}*/
