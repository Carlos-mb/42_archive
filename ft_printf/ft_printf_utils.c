/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf_utils.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/20 12:40:08 by cmelero-          #+#    #+#             */
/*   Updated: 2026/01/20 13:01:18 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

char	*ft_itoa(int n)
{
	char	*output;
	int		size;
	long	ln;
	int		isnegative;

	ln = (long)n;
	size = 0;
	isnegative = 0;
	if (ln < 0)
		size = ++isnegative;
	ln = ln * (1 - (2 * isnegative));
	size += ft_digits(ln);
	output = malloc (sizeof(char) * (size + 1));
	if (output == NULL)
		return (NULL);
	if (isnegative)
		output[0] = '-';
	output[size] = '\0';
	while (--size - isnegative >= 0)
	{
		output[size] = '0' + (ln % 10);
		ln = ln / 10;
	}
	return (output);
}

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

int	ft_digits(long n)
{
	int	size;

	size = 1;
	while (n > 9)
	{
		size++;
		n = n / 10;
	}
	return (size);
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
