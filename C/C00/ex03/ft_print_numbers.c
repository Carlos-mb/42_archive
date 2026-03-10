/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_numbers.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/06 17:07:55 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/07 11:17:28 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	ft_print_numbers(void);

/*int	main(void)
{
	ft_print_numbers();
	return (0);
}
;*/
void	ft_print_numbers(void)
{
	write (1, "0123456789", 10);
	return ;
}
