/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strncmp.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/12 16:40:19 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/17 11:00:10 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_strncmp(char *s1, char *s2, unsigned int n)
{
	unsigned int	i;

	i = 0;
	while (i < n)
	{
		if (s1[i] != s2[i] || s1[i] == '\0' )
		{
			return (s1[i] - s2[i]);
		}
		i++;
	}
	return (0);
}
/*
#include <stdio.h>
#include <string.h>
int main(void)
{
	char a[]="ARGB";
	char b[]="AG3AC";
	char c[]="CSSD3C";
	int i = 1;
	
	while (i<4)
	{
	printf("Mio  :%i\n", ft_strncmp("ARGB","AG3AC",i));
	printf("Suyo :%i\n",    strncmp("ARGB","AG3AC",i));
	printf("Mio2  :%i\n", ft_strncmp(a,c, i));
	printf("Suyo2 :%i\n", strncmp(a,c,i ));
    printf("Mio3  :%i\n", ft_strncmp(c,b,i ));
    printf("Suyo3 :%i\n", strncmp(c,b,i ));
    printf("Mio4  :%i\n", ft_strncmp(c,a,i ));
    printf("Suyo4 :%i\n", strncmp(c,a,i));
	i++;
	}

	return(0);
}
*/
