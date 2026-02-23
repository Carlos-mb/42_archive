/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf_utils.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/20 12:40:08 by cmelero-          #+#    #+#             */
/*   Updated: 2026/02/05 14:12:42 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_utoa(unsigned int n)
{
	char	*output;
	int		size;

	size = ft_digits(n);
	output = malloc (sizeof(char) * (size + 1));
	if (output == NULL)
		return (NULL);
	output[size] = '\0';
	while (--size >= 0)
	{
		output[size] = '0' + (n % 10);
		n = n / 10;
	}
	return (output);
}

size_t	ft_write_hex(uintptr_t n, const char *hex)
{
	int		count;

	count = 0;
	if (n >= 16)
	{
		count += ft_write_hex (n / 16, hex);
		count += write (1, &(hex[n % 16]), 1);
	}
	else
		count += write (1, &(hex[n]), 1);
	return (count);
}
