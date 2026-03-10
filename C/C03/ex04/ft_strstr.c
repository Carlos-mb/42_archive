/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strstr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/13 12:07:40 by cmelero-          #+#    #+#             */
/*   Updated: 2025/11/18 20:26:31 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

char	*ft_strstr(char *str, char *to_find)
{
	int	i;
	int	j;
	int	found;

	found = 0;
	i = 0;
	j = 0;
	if (to_find[i] == '\0')
		return (&str[0]);
	while (str[i] != '\0' && found == 0)
	{
		j = 0;
		while (to_find[j] != '\0' && str[i + j] == to_find[j] && found == 0)
		{
			if (str[i + j] != '\0')
				found = 1;
			j++;
		}
		i++;
	}
	if (found == 1)
		return (&str[i - 1]);
	else
		return (0);
}
/*


#include <stdio.h>
#include <string.h>
int	main(void)
{
	
	printf("Yo1:%s\n", ft_strstr("abwer","e"));
	printf("Él1:%s\n",    strstr("abwer","e"));


	printf("Yo2:%s\n", ft_strstr("abwer","x"));
	printf("Él2:%s\n",    strstr("abwer","x"));

	printf("Yo3:%s\n", ft_strstr("abwer",""));
	printf("Él3:%s\n",    strstr("abwer",""));
	
	printf("Yo4:%s\n", ft_strstr("","x"));
	printf("Él4:%s\n",    strstr("","x"));

	printf("Yo5:%s\n", ft_strstr("abwernn","er"));
	printf("Él5:%s\n",    strstr("abwernn","er"));



}*/
