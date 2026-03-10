/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strncat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/13 10:35:42 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/17 11:54:31 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

char	*ft_strncat(char *dest, char *src, unsigned int nb)
{
	unsigned int	i;
	unsigned int	j;

	i = 0;
	j = 0;
	while (dest[i] != '\0')
	{
		i++;
	}
	while (src[j] != '\0' && j < nb)
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
	char b[9] = "ABCDE";
	int i = 2;

	printf("Suyo:%s\n", strncat(a, "FGHI", i));
	printf("Mio :%s\n", ft_strncat(b, "FGHI", i));
	return (0);
}

*/
