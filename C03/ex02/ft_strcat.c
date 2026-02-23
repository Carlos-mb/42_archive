/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strcat.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/13 10:35:42 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/17 11:35:40 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

char	*ft_strcat(char *dest, char *src)
{
	int	i;
	int	j;

	i = 0;
	j = 0;
	while (dest[i] != '\0')
	{
		i++;
	}
	while (src[j] != '\0')
	{
		dest[i] = src [j];
		j++;
		i++;
	}
	dest[i] = '\0';
	return (dest);
}
/*
#include <string.h>
#include <stdio.h>
int	main(void)
{
	char a[9] = "ABCDE";
	char c[9] = "ABCDE";
	char b[2] = "FG";

	printf("Suyo:%s\n", strcat(a, "FGH"));
	printf("Mio :%s\n", ft_strcat(c, "FGH"));
//	printf("Suyo:%s\n", strcat(b, a));
//	printf("Mio :%s\n", ft_strcat(b, a));
	return (0);
}*/
