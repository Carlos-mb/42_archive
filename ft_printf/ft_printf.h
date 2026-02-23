/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 09:30:24 by cmelero-          #+#    #+#             */
/*   Updated: 2026/01/20 12:58:53 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H

# include <stdlib.h>
# include <unistd.h>
# include <stdarg.h>
# include <stdint.h>

int		ft_printf(char const *text, ...);
size_t	ft_print_char(size_t *p_i, va_list args);
size_t	ft_print_p(size_t *p_i, va_list args);
size_t	ft_print_d_i(size_t *p_i, va_list args);
size_t	ft_print_u(size_t *p_i, va_list args);
int		ft_print_x(size_t *p_i, va_list args, const char *hex);
char	*ft_itoa(int n);
char	*ft_utoa(unsigned int n);
int		ft_digits(long n);
size_t	ft_write_hex(uintptr_t n, const char *hex);

#endif