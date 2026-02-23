/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_utils.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/20 11:29:46 by cmelero-          #+#    #+#             */
/*   Updated: 2026/01/20 11:49:41 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

t_list_gnl	*ft_lst_new(void)
{
	t_list_gnl	*output;

	output = malloc(sizeof(t_list_gnl));
	if (!(output))
		return (NULL);
	output->text[0] = '\0';
	output->pos = 0;
	output->next = NULL;
	return (output);
}

void	ft_lst_clear(t_list_gnl **lst)
{
	void	*tmp;

	while (*lst)
	{
		tmp = (*lst)->next;
		free(*lst);
		*lst = tmp;
	}
	*lst = NULL;
}

size_t	ft_getsize(t_list_gnl *current)
{
	size_t	i;

	i = 0;
	while (current && current->text[0] != '\0')
	{
		i += current->pos;
		current = (current)->next;
	}
	return (i);
}
