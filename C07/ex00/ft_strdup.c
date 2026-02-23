/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/21 08:22:25 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/21 10:53:50 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>

char	*ft_strdup(char *src)
{
	char	*des;
	int		i;

	i = 0;
	while (src[i] != '\0')
		i++;
	des = malloc((i + 1));
	if (des == NULL)
		return (NULL);
	i = 0;
	while (src[i] != '\0')
	{
		des[i] = src[i];
		i++;
	}
	des[i] = '\0';
	return (des);
}
/*
#include <unistd.h>

int main (void)
{
	char *ori;
	char *c = ft_strdup ("Hola, caracola, \nesto está del revés");
	ori = c;
	while (*c != '\0')
		write (1, c++, 1);

	free (ori);
	return (0);
}*/
