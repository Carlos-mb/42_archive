/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/13 13:38:21 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/18 21:09:12 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

unsigned int	len(char *str)
{
	int	i;

	i = 0;
	while (str[i] != '\0')
	{
		i++;
	}
	return (i);
}

unsigned int	ft_strlcat(char *dest, char *src, unsigned int size)
{
	unsigned int	len_dest;
	unsigned int	len_src;
	unsigned int	i;
	unsigned int	sum;

	len_dest = len(dest);
	len_src = len(src);
	if (len_src <= size)
		sum = len_src + len_dest;
	else
		sum = len_dest + size;
	i = 0;
	while (src[i] != '\0' && len_dest < (size - 1))
	{
		dest[len_dest] = src[i];
		len_dest++;
		i++;
	}
	dest [len_dest] = '\0';
	return (sum);
}
/*

#include <bsd/string.h>
#include <stdio.h>

int main(void)
{
	char dest[6]="123";
	char dest2[6]="123";
	
	printf("return:%zu\n",strlcat (dest, "456", 6));
	printf("bueno :%s<\n",dest);

	printf ("return:%u\n",ft_strlcat (dest2, "456", 6	));
	printf("mio   :%s<", dest2);
}*/
