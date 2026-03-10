/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strupcase.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/12 13:32:36 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/12 15:20:00 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//#include <stdio.h>
#include <unistd.h>

char	*ft_strupcase(char *str)
{
	int		i;
	char	*c;

	c = str;
	i = 0;
	while (str[i] != '\0')
	{
		if (str[i] >= 'a' && str[i] <= 'z')
		{
			str[i] = str[i] - 32;
		}
		i++;
	}
	str = c;
	return (str);
}
/*
int	main(void)
{
	char c[] = "AssD333";
	printf("%s\n",c);
	ft_strupcase(c);
	printf("%s\n",c);
	return (0);
}*/
