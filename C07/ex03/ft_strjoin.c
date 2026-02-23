/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strjoin.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/25 09:01:48 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/25 11:56:02 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include <stdlib.h>
//#include <stdio.h>
//#include <unistd.h>

int	ft_arrsize(char *c)
{
	int	i;

	i = 0;
	while (c[i] != 0)
		i++;
	return (i);
}

char	*ft_strjoin(int size, char **strs, char *sep)
{
	char	*salida;
	int		i;
	int		j;
	int		total;

	i = 0;
	j = 1;
	while (i < size)
		j += ft_arrsize(strs[i++]);
	if (size > 0)
		j += ft_arrsize(sep) * (size - 1);
	salida = malloc(sizeof(char) * j);
	i = -1;
	total = 0;
	while (++i < size)
	{
		j = 0;
		while (strs[i][j] != '\0')
			salida[total++] = strs[i][j++];
		j = 0;
		while (sep[j] != 0 && i + 1 < size)
			salida[total++] = sep[j++];
	}
	salida[total] = '\0';
	return (salida);
}
/*
int	main(void)
{
	char	*resultado;
	char	*prueba[4] = {"abcd", "efgh", "ijk"};
	char	*pruebaerror;
	
	resultado = ft_strjoin (0, prueba, "-|-");
	printf("salida: %s", resultado);
	free (resultado);

	resultado = ft_strjoin (3, prueba, "-|-");
	printf("salida: %s", resultado);
	free (resultado);
}*/
