/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_atoi.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/19 07:38:45 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/20 16:05:19 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_is_minus(char *str, int *i)
{
	int	menos;

	menos = 1;
	*i = 0;
	while (str[*i] == ' ' || (str[*i] >= 9 && str[*i] <= 13))
		*i = *i + 1;
	while (str[*i] == '-' || str[*i] == '+')
	{
		if (str[*i] == '-')
			menos = -menos;
		*i = *i + 1;
	}
	return (menos);
}

int	ft_extract_number(char *str)
{
	int	i;
	int	salida;

	salida = 0;
	i = 0;
	while (str[i] >= '0' && str[i] <= '9' && str[i] != '\0')
	{
		salida = salida * 10;
		salida += str[i] - '0';
		i++;
	}
	return (salida);
}

int	ft_atoi(char *str)
{
	int	i;
	int	menos;

	i = 0;
	menos = ft_is_minus (str, &i);
	return (ft_extract_number(&str[i]));
}
/*
#include <stdio.h>
int	main (void)
{

	printf("%i\n", ft_atoi("   \n   ----5801"));
	printf("=========\n");
	printf("%i\n", ft_atoi("   \n   ----58kk"));
	printf("%i\n", ft_atoi("   \n   ---1607890kk"));
	printf("%i\n", ft_atoi("   \n   ---0940321kk"));	


}	*/
