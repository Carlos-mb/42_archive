/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion_setup_impl.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/03 18:50:00 by cmelero-          #+#    #+#             */
/*   Updated: 2026/05/05 15:45:55 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	ft_init_simulation_cleanup(t_simulation *sim,
	int status)
{
	int	i;

	if (status <= 1)
		pthread_mutex_destroy(&sim->state_mutex);
	if (status <= 2)
		pthread_mutex_destroy(&sim->log_mutex);
	if (status <= 3)
		pthread_mutex_destroy(&sim->cond_mutex);
	if (status <= 4)
	{
		i = sim->config.ncod;
		while (--i >= 0)
			pthread_mutex_destroy(&sim->dongles[i].mutex);
		free(sim->dongles);
		sim->dongles = NULL;
	}
	free(sim->coders);
	return (0);
}

static int	ft_init_simulation_fill_coders(t_simulation *sim)
{
	int	i;

	i = 0;
	while (i < sim->config.ncod)
	{
		sim->coders[i].id = i + 1;
		sim->coders[i].ld = &(sim->dongles[i]);
		sim->coders[i].compilations = 0;
		sim->coders[i].sim = sim;
		sim->coders[i].thread = 0;
		sim->coders[i].burned = 0;
		sim->coders[i].ended = 0;
		sim->coders[i].last_compile_start = 0;
		if (pthread_mutex_init(&sim->coders[i].mutex, NULL) != 0)
			return (0);
		if (i == sim->config.ncod -1)
			sim->coders[i].rd = &(sim->dongles[0]);
		else
			sim->coders[i].rd = &(sim->dongles[i + 1]);
		i++;
	}
	return (1);
}

int	ft_init_simulation_impl(t_simulation *sim)
{
	sim->started = 0;
	sim->stop_now = 0;
	sim->monitor_thread = 0;
	sim->coders = malloc(sizeof(t_coder) * sim->config.ncod);
	if (!sim->coders || (pthread_cond_init(&(sim->cond), NULL) != 0))
		return (0);
	if (pthread_mutex_init(&(sim->log_mutex), NULL) != 0)
		return (ft_init_simulation_cleanup(sim, 0));
	if (pthread_mutex_init(&(sim->state_mutex), NULL) != 0)
		return (ft_init_simulation_cleanup(sim, 1));
	if (pthread_mutex_init(&(sim->cond_mutex), NULL) != 0)
		return (ft_init_simulation_cleanup(sim, 2));
	if (!ft_init_dongles(sim, sim->config.ncod))
		return (ft_init_simulation_cleanup(sim, 3));
	if (!ft_init_simulation_fill_coders(sim))
		return (ft_init_simulation_cleanup(sim, 4));
	return (1);
}
