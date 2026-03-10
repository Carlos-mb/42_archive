/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_is_negative.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/06 17:07:55 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/10 10:09:09 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	ft_is_negative(int n);

/*int	main(void)
{
	ft_is_negative(5);
	ft_is_negative(-1);
	ft_is_negative(0);
	return (0);
}*/
void	ft_is_negative(int n)
{
	if (n > 0)
	{
		write(1, "P", 1);
	}
	else if (n < 0)
	{
		write(1, "N", 1);
	}
	else
	{
		write(1, "P", 1);
	}
	return ;
}
