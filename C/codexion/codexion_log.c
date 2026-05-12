/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion_log.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/03 18:50:00 by cmelero-          #+#    #+#             */
/*   Updated: 2026/05/05 12:16:25 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	ft_wakeup(t_simulation *sim)
{
	pthread_mutex_lock(&(sim->cond_mutex));
	pthread_cond_broadcast(&(sim->cond));
	pthread_mutex_unlock(&(sim->cond_mutex));
}

void	ft_log_burned(t_coder *coder, const char *string)
{
	if (pthread_mutex_lock(&((coder->sim)->log_mutex)) == 0)
	{
		printf("%lld %d %s\n",
			ft_now() - coder->sim->started,
			coder->id,
			string);
		pthread_mutex_unlock(&(coder->sim->log_mutex));
	}
	ft_wakeup(coder->sim);
}

int	ft_log(t_coder *coder, const char *string)
{
	if (pthread_mutex_lock(&((coder->sim)->log_mutex)) == 0)
	{
		if (!ft_stop_read(coder->sim) || coder->sim->config.debug)
		{
			printf("%lld %d %s\n",
				ft_now() - coder->sim->started,
				coder->id,
				string);
		}
		pthread_mutex_unlock(&(coder->sim->log_mutex));
	}
	return (1);
}
