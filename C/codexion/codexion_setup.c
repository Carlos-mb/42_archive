/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion_setup.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/03 18:50:00 by cmelero-          #+#    #+#             */
/*   Updated: 2026/05/05 15:27:34 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	ft_init_simulation(t_simulation *sim)
{
	return (ft_init_simulation_impl(sim));
}

void	ft_free_simulation(t_simulation *sim)
{
	pthread_mutex_destroy(&(sim->log_mutex));
	pthread_mutex_destroy(&(sim->state_mutex));
	pthread_mutex_destroy(&(sim->cond_mutex));
	pthread_cond_destroy(&sim->cond);
	ft_free_mutex(sim);
	free(sim->coders);
}

int	ft_start_threads(t_simulation *sim)
{
	int	i;

	i = 0;
	while (i < sim->config.ncod)
	{
		sim->coders[i].last_compile_start = sim->started;
		if (pthread_create(&(sim->coders[i].thread), NULL,
				ft_thread_coder, &(sim->coders[i])) != 0)
			return (0);
		i++;
	}
	if (pthread_create(&(sim->monitor_thread), NULL,
			ft_thread_monitor, sim) != 0)
		return (0);
	return (1);
}

int	ft_start_simulation(t_simulation *sim)
{
	int	out;

	sim->started = ft_now();
	out = ft_start_threads(sim);
	return (out);
}

int	ft_run_simulation(t_simulation *sim)
{
	int	i;

	i = 0;
	while (i < sim->config.ncod)
	{
		if (sim->coders[i].thread)
			pthread_join(sim->coders[i].thread, NULL);
		i++;
	}
	if (sim->monitor_thread)
		pthread_join(sim->monitor_thread, NULL);
	return (0);
}
