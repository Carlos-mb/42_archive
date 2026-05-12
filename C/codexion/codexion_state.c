/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion_state.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/03 18:50:00 by cmelero-          #+#    #+#             */
/*   Updated: 2026/05/05 11:07:38 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

char	ft_stop_read(t_simulation *sim)
{
	char	out;

	out = 0;
	if (pthread_mutex_lock(&(sim->state_mutex)) == 0)
	{
		out = sim->stop_now;
		pthread_mutex_unlock(&(sim->state_mutex));
	}
	return (out);
}

void	ft_stop(t_simulation *sim)
{
	if (pthread_mutex_lock(&(sim->state_mutex)) == 0)
	{
		sim->stop_now = 1;
		pthread_mutex_unlock(&(sim->state_mutex));
		pthread_mutex_lock(&(sim->cond_mutex));
		pthread_cond_broadcast(&(sim->cond));
		pthread_mutex_unlock(&(sim->cond_mutex));
	}
	return ;
}

int	ft_read_compilations(t_coder *coder)
{
	int	out;

	pthread_mutex_lock(&(coder->sim->state_mutex));
	out = coder->compilations;
	pthread_mutex_unlock(&(coder->sim->state_mutex));
	return (out);
}
