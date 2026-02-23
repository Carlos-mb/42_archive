/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/08 12:39:02 by cmelero-          #+#    #+#             */
/*   Updated: 2026/01/20 12:59:00 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static size_t	ft_print_s(size_t *p_i, va_list args)
{
	char	*c;
	size_t	count;

	(*p_i) += 1;
	c = va_arg(args, char *);
	if (!c)
	{
		count = write(1, "(null)", 6);
	}
	else
	{
		count = 0;
		while (*c)
		{
			count += write(1, c, 1);
			c++;
		}
	}
	return (count);
}

static size_t	ft_print_this(char const *text, size_t *p_i, va_list args)
{
	size_t	count;

	count = 0;
	if (text[*p_i] != '%')
		return (write (1, &(text[*p_i]), 1));
	else if (text[*p_i] == '%' && text[(*p_i) + 1] == '%')
		return (write(1, &(text[(*p_i)++]), 1));
	else if (text[*p_i] == '%' && text[(*p_i) + 1] == 'c')
		return (ft_print_char(p_i, args));
	else if (text[*p_i] == '%' && text[(*p_i) + 1] == 's')
		return (ft_print_s(p_i, args));
	else if (text[*p_i] == '%' && text[(*p_i) + 1] == 'p')
		return (ft_print_p(p_i, args));
	else if (text[*p_i] == '%' && text[(*p_i) + 1] == 'd')
		return (ft_print_d_i(p_i, args));
	else if (text[*p_i] == '%' && text[(*p_i) + 1] == 'i')
		return (ft_print_d_i(p_i, args));
	else if (text[*p_i] == '%' && text[(*p_i) + 1] == 'u')
		return (ft_print_u(p_i, args));
	else if (text[*p_i] == '%' && text[(*p_i) + 1] == 'x')
		return (ft_print_x(p_i, args, "0123456789abcdef"));
	else if (text[*p_i] == '%' && text[(*p_i) + 1] == 'X')
		return (ft_print_x(p_i, args, "0123456789ABCDEF"));
	return (count);
}

int	ft_printf(char const *text, ...)
{
	va_list	args;
	size_t	i;
	size_t	count;

	if (!text)
		return (-1);
	va_start (args, text);
	i = 0;
	count = 0;
	while (text[i])
	{
		count = count + ft_print_this(text, &i, args);
		i++;
	}
	va_end (args);
	return (count);
}
/*
#include <stdio.h>
#include <limits.h>
// cspdiuxX%
int	xmain(void)
{

	printf("---\n");
	printf("%d", ft_printf(NULL, NULL));
	printf("\n---\n");
	printf("%d", printf(NULL, NULL));
*/
	/*
	size_t n = 0;
	n = ft_printf(" %i ", NULL, 0);	
	printf("%d", n);
	printf("\n");
	printf("%d", printf(" %p %p ", 0, 0));
//	printf("\n");

	return 0;
}*/
/*
//	ft_printf(a);

printf("Al loro con esto...\n");
	write(1, "á", 1);
	write(1, "á", 2);	
	printf("\n===\n");
	printf("Y sin salto de línea....(¡lo pone antes pq tiene un buffer!)");
	write(1, "á", 1);
	write(1, "á", 2);	
	printf("\n===\n");

	printf("[%d]", ft_printf("á"));
	printf("\n---\n");
	printf("[%d]",    printf("á"));
	printf("\n---\n");

	char a[] = "1234\n12345\n";
	printf("[%d]", ft_printf(a));
	printf("\n---\n");
	printf("[%d]",    printf(a));
	printf("\n---\n");

	printf("[%d]", ft_printf("%%<-here\n"));
	printf("\n---\n");
	printf("[%d]",    printf("%%<-here\n"));
	printf("\n---\n");
	
	char b[] = "Esto es un char >%c<, a ver qué tal";
	printf("[%d]", ft_printf(b, '*'));
	printf("\n---\n");
	printf("[%d]",    printf(b, '*'));
	printf("\n---\n");

	char c[] = "Esto es un error de char >%c<, a ver qué tal";
	printf("[%d]", ft_printf(c, "Hola"));
	printf("\n---\n");
	printf("[%d]",    printf(c, "Hola"));	
	printf("\n---\n");

	char d[] = "á%c ";
	printf("[%d]", ft_printf(d, '*'));
	printf("\n---\n");
	printf("[%d]",    printf(d, '*'));
	printf("\n---\n");	

	char e[] = "char >%c< y string >%s<, fin";
	printf("[%d]", ft_printf(e, '1', "String"));
	printf("\n---\n");
	printf("[%d]",    printf(e, '1', "String"));	
	printf("\n---\n");

	printf("Char y string juntos:\n");
	char f[] = "%c%s";
	printf("[%d]", ft_printf(f, '1', "String"));
	printf("\n---\n");
	printf("[%d]",    printf(f, '1', "String"));	l
	printf("\n---\n");


	char g[] = "char >%c< y puntero >p%pp<, fin";
	printf("[%d]", ft_printf(g, '1', &g));
	printf("\n---\n");
	printf("[%d]",    printf(g, '1', &g));	
	printf("\n---\n");

	char h[] = "I int >%i< y puntero >p%pp<, fin";
	printf("[%d]", ft_printf(h, 155, &h));
	printf("\n---\n");
	printf("[%d]",    printf(h, 155, &h));	
	printf("\n---\n");

	char i[] = "I2 int malo >%i< y puntero >p%pp<, fin";
	printf("[%d]", ft_printf(i, 1513241234123412435, &i));
	printf("\n---\n");
	printf("[%d]",    printf(i, 1513241234123412435, &i));	
	printf("\n---\n");

	char j[] = "D int >%d< y puntero >p%pp<, fin";
	printf("[%d]", ft_printf(j, 155, &j));
	printf("\n---\n");
	printf("[%d]",    printf(j, 155, &j));	
	printf("\n---\n");
	
	char k[] = "D2 con int malo >%d< y puntero >p%pp<, fin";
	printf("[%d]", ft_printf(k, 1513241234123412435, &k));
	printf("\n---\n");
	printf("[%d]",    printf(k, 1513241234123412435, &k));	
	printf("\n---\n");

	char l[] = "U int >%u< y puntero >p%pp<, fin";
	printf("[%d]", ft_printf(l, 155, &l));
	printf("\n---\n");
	printf("[%d]",    printf(l, 155, &l));	
	printf("\n---\n");
	
	char m[] = "u2 con int malo >%u< y puntero >p%pp<, fin";
	printf("[%d]", ft_printf(m, -15132, &m));
	printf("\n---\n");
	printf("[%d]",    printf(m, -15132, &m));	
	printf("\n---\n");	

	char n[] = "x int >%x< >%x< y puntero >p%pp<, fin";
	printf("[%d]", ft_printf(n, 259155, 1, &n));
	printf("\n---\n");
	printf("[%d]",    printf(n, 259155, 1, &n));	
	printf("\n---\n");
	
	char o[] = "x2 con int malo >%x< y puntero >p%pp<, fin";
	printf("[%d]", ft_printf(o, -15132, &o));
	printf("\n---\n");
	printf("[%d]",    printf(o, -15132, &o));	
	printf("\n---\n");

	char p[] = "X int >%X< >%X< y puntero >p%pp<, fin";
	printf("[%d]", ft_printf(p, 259155, 1, &p));
	printf("\n---\n");
	printf("[%d]",    printf(p, 259155, 1, &p));	
	printf("\n---\n");
	
	char q[] = "X2 con int malo >%X< y puntero >p%pp<, fin";
	printf("[%d]", ft_printf(q, -15132, &q));
	printf("\n---\n");
	printf("[%d]",    printf(q, -15132, &q));	
	printf("\n---\n");	
	
	char ch = 'A';
	char *str = "string";
	int i = -42;
	int j = -42;
	unsigned int u = 42;
    int count;
    count = 0;
	//Test 1: c, s, d, i
	printf("Test1\n");
	count = ft_printf("%s  %c  %d  %i\n", str, ch, i, i);
	printf("ft_printf count = %d\n\n", count);
	count = printf("%s  %c  %d  %i\n", str, ch, i, i);
    printf("printf count = %d\n\n\n", count);
	//Test 2: p
	printf("Test2\n\n");
    count = ft_printf("p: %p\n\n", str);
	printf("ft_printf count = %d\n\n", count); 
	count = printf("p: %p\n\n", str);
	printf("printf count = %d\n\n\n", count);
	//Test 3: u
	printf("Test3\n");
    count = ft_printf("unsigned: %u\n", u);
	printf("ft_printf count = %d\n\n", count);
	count = printf("unsigned: %u\n", u);
	printf("printf count = %d\n\n\n", count);
	//Test 4: u but sending negative int
	printf("Test4\n");
    count = ft_printf("unsigned: %u\n", j);
	printf("ft_printf count = %d\n\n", count);
	count = printf("unsigned: %u\n", j);
	printf("printf count = %d\n\n\n", count);
	//Test 5: x
	printf("Test5\n");
	count = ft_printf("hex: %x\n", i);
	printf("ft_printf count = %d\n\n", count);
	ft_printf("hex: %x\n", i);
	printf("printf count = %d\n\n\n", count);
	//Test 6: X
	printf("Test6\n");
	count = ft_printf("hex: %X\n", i);
	printf("ft_printf count = %d\n\n", count);
	ft_printf("hex: %X\n", i);
	printf("printf count = %d\n\n\n", count);
	//Test 7: %%
	printf("Test7\n");
	count = ft_printf("percentage %%\n");
	printf("ft_printf count = %d\n\n", count);
	count = printf("percentage %%\n");
	printf("printf count = %d\n\n\n", count);
	//Test 8: %j - an invalid argument
	printf("Test8\n");
    count = ft_printf("f%jk\n", i);
	printf("ft_printf count = %d\n\n", count);
	count = printf("f%jk\n", i);
	printf("printf count = %d\n\n\n", count);
	//Test 9: s (null)
	printf("Test9\n");
	count = ft_printf(" NULL %s NULL\n", NULL);
	printf("ft_printf count = %d\n\n", count);
	count = printf(" NULL %s NULL\n", NULL);
	printf("printf count = %d\n\n\n", count);
	//Test 10: s (sending 0)
	printf("Test10\n");
	count = ft_printf(" NULL %s NULL\n", 0);
	printf("ft_printf count = %d\n\n", count);
	count = printf(" NULL %s NULL\n", 0);
	printf("printf count = %d\n\n\n", count);
	//Test 11: p (long address)
	//(long) LONG_MAX: 2147483647;  LONG_MIN: -2147483648;
	printf("Test11\n");
	count = ft_printf(" %p %p \n", LONG_MIN, LONG_MAX);
	printf("ft_printf count = %d\n\n", count);
	count = printf(" %p %p \n", LONG_MIN, LONG_MAX);
	printf("printf count = %d\n\n\n", count);
	//Test 12: p (unsigned long address)
	printf("Test12\n");
	count = ft_printf(" %p %p \n", ULONG_MAX, -ULONG_MAX);
	printf("ft_printf count = %d\n\n", count);
	count = printf(" %p %p \n", ULONG_MAX, -ULONG_MAX);
	printf("printf count = %d\n\n\n", count);
	//Test 13: p (nil) (sending 0)
	printf("Test13\n");
	count = ft_printf(" %p %p \n", 0, 0);
	printf("ft_printf count = %d\n\n", count);
	count = printf(" %p %p \n", 0, 0);
	printf("printf count = %d\n\n\n", count);
	//Test 14: hex (sending 0)
	printf("Test14\n");
	count = ft_printf(" %x %x \n", 0, 0);
	printf("ft_printf count = %d\n\n", count);
	count = printf(" %x %x \n", 0, 0);
	printf("printf count = %d\n\n\n", count);
	//Test 15: with no arguments
	printf("Test15\n");
	count = ft_printf("Hi %d Hai\n");
	printf("ft_printf count = %d\n\n", count);
	count = printf("Hi %d Hai\n");
	printf("printf count = %d\n\n\n", count);
	//Test 16
	//undefined behavior, it can lead to seg fault or crash
	printf("Test16\n");
	count = ft_printf(NULL);
	printf("ft_printf count = %d\n\n\n", count);
	count = printf(NULL);
	printf("printf count = %d\n\n", count);
	//string/Test 17
	printf("Test17\n");
	count = ft_printf("%s\n", "");
	printf("ft_printf count = %d\n\n", count);
	count = printf("%s\n", "");
	printf("printf count = %d\n", count);

	return (1);
}
*/
