/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_range.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/21 10:58:15 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/25 08:33:01 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>
#include <unistd.h>

int	*ft_range(int min, int max)
{
	int	*valores;
	int	i;

	if (min >= max)
		return (NULL);
	valores = malloc((max - min) * sizeof(int));
	if (valores == NULL)
		return (NULL);
	i = 0;
	while (min < max)
		valores[i++] = min++;
	return (valores);
}
/*
#include <unistd.h>
#include <stdio.h>

int main(void)
{
	int				*valores = ft_range(0, 10);
	unsigned long	i = -1;
//	printf("%lu\n", 10);

	while (++i < 10)
		printf("%lu:%i\n", i, valores[i]);
}*/
