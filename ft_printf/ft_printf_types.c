/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf_types.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/20 12:44:18 by cmelero-          #+#    #+#             */
/*   Updated: 2026/01/20 13:01:27 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

size_t	ft_print_char(size_t *p_i, va_list args)
{
	char	c;
	int		i;

	i = va_arg(args, int);
	c = (char) i;
	(*p_i) += 1;
	return (write(1, &c, 1));
}

size_t	ft_print_p(size_t *p_i, va_list args)
{
	void		*p;
	uintptr_t	value;
	size_t		count;

	p = va_arg(args, void *);
	if (!p)
	{
		count = write(1, "(nil)", 5);
	}
	else
	{
		value = (uintptr_t) p;
		count = write (1, "0x", 2);
		count += ft_write_hex(value, "0123456789abcdef");
	}
	(*p_i) += 1;
	return (count);
}

size_t	ft_print_d_i(size_t *p_i, va_list args)
{
	int		n;
	char	*c_value;
	size_t	count;
	int		j;

	n = va_arg(args, int);
	c_value = ft_itoa (n);
	if (!c_value)
		return (0);
	(*p_i) += 1;
	count = 0;
	j = 0;
	while (c_value[j])
	{
		count += write(1, &c_value[j], 1);
		j++;
	}
	free (c_value);
	return (count);
}

size_t	ft_print_u(size_t *p_i, va_list args)
{
	unsigned int	n;
	char			*c_value;
	size_t			count;
	int				j;

	n = va_arg(args, unsigned int);
	c_value = ft_utoa (n);
	if (!c_value)
		return (0);
	(*p_i) += 1;
	count = 0;
	j = 0;
	while (c_value[j])
	{
		count += write(1, &c_value[j], 1);
		j++;
	}
	free (c_value);
	return (count);
}

int	ft_print_x(size_t *p_i, va_list args, const char *hex)
{
	unsigned int	n;

	n = va_arg(args, unsigned int);
	(*p_i) += 1;
	return (ft_write_hex(n, hex));
}
