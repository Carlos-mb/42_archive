/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.h                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/20 11:39:17 by cmelero-          #+#    #+#             */
/*   Updated: 2026/01/20 11:39:17 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef GET_NEXT_LINE_H
# define GET_NEXT_LINE_H

# ifndef BUFFER_SIZE
#  define BUFFER_SIZE 10
# endif

# include <stdlib.h>
# include <unistd.h>

typedef struct s_list
{
	char			text [BUFFER_SIZE + 1];
	size_t			pos;
	struct s_list	*next;		
}					t_list_gnl;

char		*get_next_line(int fd);
t_list_gnl	*ft_lst_new(void);
void		ft_lst_clear(t_list_gnl **lst);
size_t		ft_getsize(t_list_gnl *current);

#endif