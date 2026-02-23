/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/20 11:10:24 by cmelero-          #+#    #+#             */
/*   Updated: 2026/01/23 11:39:15 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

static int	ft_read_char(int fd, char *buffer, char *c_read)
{
	ssize_t	bytes_read;
	size_t	i;

	if (buffer[0] == '\0')
	{
		bytes_read = read (fd, buffer, BUFFER_SIZE);
		if (bytes_read < 0)
			return (-1);
		else
			buffer[bytes_read] = '\0';
	}
	*c_read = buffer[0];
	i = 0;
	while (buffer[i] != '\0')
	{
		buffer[i] = buffer [i + 1];
		i++;
	}
	return (1);
}

static int	ft_add_char(char c_read, t_list_gnl **p_current_text)
{
	t_list_gnl	*new_text;

	if ((*p_current_text)->pos == BUFFER_SIZE)
	{
		new_text = ft_lst_new();
		if (!new_text)
			return (0);
		(*p_current_text)->next = new_text;
		(*p_current_text) = new_text;
	}
	(*p_current_text)->text[(*p_current_text)->pos] = c_read;
	(*p_current_text)->text[((*p_current_text)->pos) + 1] = '\0';
	(*p_current_text)->pos += 1;
	(*p_current_text)->next = NULL;
	return (1);
}

static char	*ft_create_output(t_list_gnl *out_list)
{
	size_t		i;
	size_t		j;
	t_list_gnl	*current;
	char		*output;

	i = ft_getsize(out_list);
	if (i > 0)
	{
		output = malloc (sizeof(char) * (i + 1));
		i = 0;
		current = out_list;
		while (output && current)
		{
			j = 0;
			while ((current->text)[j])
				output [i++] = (current->text)[j++];
			output[i] = '\0';
			current = (current)->next;
		}
	}
	else
		output = NULL;
	ft_lst_clear(&out_list);
	return (output);
}

char	*get_next_line(int fd)
{
	char		c_read;
	static char	buffer [BUFFER_SIZE + 1];
	t_list_gnl	*out_list;
	t_list_gnl	*current_text;
	int			readed;

	if (fd < 0)
		return (NULL);
	out_list = ft_lst_new ();
	if (!out_list)
		return (NULL);
	current_text = out_list;
	c_read = ' ';
	readed = 1;
	while (c_read != '\n' && c_read != '\0' && readed > 0 && out_list)
	{
		readed = ft_read_char(fd, buffer, &c_read);
		if ((readed >= 0) && (c_read != '\0'))
			if (!ft_add_char(c_read, &current_text))
				ft_lst_clear(&out_list);
		if (readed < 0)
			ft_lst_clear(&out_list);
	}
	return (ft_create_output(out_list));
}
