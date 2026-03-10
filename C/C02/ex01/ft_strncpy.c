/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strncpy.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/12 09:57:33 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/12 15:08:06 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

char	*ft_strncpy(char *dest, char *src, unsigned int n)
{
	int				end;
	unsigned int	i;
	char			*tmp;

	i = 0;
	end = 0;
	tmp = dest;
	while (i < n)
	{
		if (end || (*src == '\0'))
		{
			end = 1;
			*dest = '\0';
			dest++;
		}
		else
		{
			*dest = *src;
			dest++;
			src++;
		}
		i++;
	}
	return (tmp);
}
/*
int	main(void)
{
	char dest[]="adios";
	char src[]="Hola";
	char dest2[]="adios";
	char src2[]="Hola";
	char *tmp;

	write (1, "la buena:",10);
	tmp = ft_strncpy(dest, src, 3);
	write(1, tmp,5);
	write (1, "\nla mia   :", 10);
	tmp = ft_strncpy(dest2, src2, 3);
	write(1, tmp, 5);
}
*/
