/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion_threads.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/03 18:50:00 by cmelero-          #+#    #+#             */
/*   Updated: 2026/05/05 15:36:02 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	*ft_thread_monitor(void *sim_in)
{
	return (ft_thread_monitor_impl(sim_in));
}

void	*ft_thread_coder(void *coder_in)
{
	return (ft_thread_coder_impl(coder_in));
}

void	*ft_thread_monitor_impl(t_simulation *sim)
{
	int				compiled;
	char			stop;

	while (ft_actived_coders(sim))
	{
		stop = 0;
		compiled = 0;
		ft_thread_monitor_scan(sim, &compiled, &stop);
		if (compiled == sim->config.compiles_required
			* sim->config.ncod)
			ft_stop(sim);
		ft_dongle_monitor_scan(sim);
		usleep(SLEEP);
	}
	return (NULL);
}

void	*ft_thread_coder_impl(t_coder *coder)
{
	while (!ft_stop_read(coder->sim)
		&& ft_read_compilations(coder) < coder->sim->config.compiles_required)
	{
		ft_compile_cycle(coder);
		if (ft_read_compilations(coder) < coder->sim->config.compiles_required)
			ft_thread_wait(coder, ft_now(), coder->sim->config.time_to_debug,
				"is debugging");
		if (ft_read_compilations(coder) < coder->sim->config.compiles_required)
			ft_thread_wait(coder, ft_now(), coder->sim->config.time_to_refactor,
				"is refactoring");
	}
	pthread_mutex_lock(&(coder->mutex));
	coder->ended = 1;
	pthread_mutex_unlock(&(coder->mutex));
	return (NULL);
}
