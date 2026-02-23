/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strcmp.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/12 16:40:19 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/17 11:00:42 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_strcmp(char *s1, char *s2)
{
	int	i;

	i = 0;
	while (s1[i] == s2[i] && s1[i])
	{
		i++;
	}
	return (s1[i] - s2[i]);
}

/*
#include <stdio.h>
#include <string.h>

int main(void)
{
//	char a[]="AB";
//	char b[]="AAC";
//	char c[]="CC";
	
	printf("Mio  :%i\n", ft_strcmp("AB","AB"));
	printf("Suyo :%i\n",    strcmp("AB","AB"))	;

	printf("Mio1  :%i\n", ft_strcmp("AB","AAC"));
	printf("Suyo1 :%i\n",    strcmp("AB","AAC"));

	printf("Mio2  :%i\n", ft_strcmp("AB","CC"));
	printf("Suyo2 :%i\n",    strcmp("AB","CC"));

    printf("Mio3  :%i\n", ft_strcmp("CC","ACC"));
    printf("Suyo3 :%i\n",    strcmp("CC","ACC"));

    printf("Mio4  :%i\n", ft_strcmp("ACC","AB"));
    printf("Suyo4 :%i\n",    strcmp("ACC","AB"));


	return(0);
}
*/
