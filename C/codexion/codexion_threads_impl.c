/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion_threads_impl.c                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/03 18:50:00 by cmelero-          #+#    #+#             */
/*   Updated: 2026/05/05 15:39:34 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

char	ft_thread_wait(t_coder *coder,
	long long time,
	long long pause,
	const char *string)
{
	char		stopped;

	stopped = 0;
	if (string)
		ft_log(coder, string);
	while (!stopped && ft_now() - time < pause)
	{
		if (ft_stop_read(coder->sim))
			stopped = 1;
		else
			usleep(SLEEP);
	}
	return (stopped);
}

void	ft_thread_monitor_scan(t_simulation *sim, int *compiled,
	char *stop)
{
	int			i;
	int			burned_index;
	long long	now;

	i = 0;
	burned_index = -1;
	now = ft_now();
	if (pthread_mutex_lock(&(sim->state_mutex)) != 0)
		return ;
	while (i < sim->config.ncod && !*stop)
	{
		*compiled += sim->coders[i].compilations;
		if (sim->coders[i].compilations < sim->config.compiles_required
			&& sim->coders[i].last_compile_start
			+ sim->config.time_to_burnout <= now)
		{
			sim->stop_now = 1;
			*stop = 1;
			burned_index = i;
		}
		i++;
	}
	pthread_mutex_unlock(&(sim->state_mutex));
	if (burned_index >= 0)
		ft_log_burned(&(sim->coders[burned_index]), "burned out");
}

void	ft_dongle_monitor_scan(t_simulation *sim)
{
	int			i;

	i = 0;
	while (i < sim->config.ncod)
	{
		pthread_mutex_lock(&(sim->dongles[i].mutex));
		if (ft_now() >= sim->dongles[i].cooldown_until_ms)
			ft_wakeup(sim);
		pthread_mutex_unlock(&(sim->dongles[i].mutex));
		i++;
	}
}

int	ft_actived_coders(t_simulation *sim)
{
	int	i;

	i = 0;
	while (i < sim->config.ncod)
	{
		pthread_mutex_lock(&sim->coders[i].mutex);
		if (!sim->coders[i].ended)
		{
			pthread_mutex_unlock(&sim->coders[i].mutex);
			return (1);
		}
		pthread_mutex_unlock(&sim->coders[i].mutex);
		i++;
	}
	return (0);
}

int	ft_compile_cycle(t_coder *coder)
{
	while (!ft_stop_read(coder->sim) && !ft_take_dongles(coder))
	{
		pthread_mutex_lock(&(coder->sim->cond_mutex));
		pthread_cond_wait(&coder->sim->cond, &coder->sim->cond_mutex);
		pthread_mutex_unlock(&(coder->sim->cond_mutex));
	}
	if (!ft_stop_read(coder->sim))
	{
		pthread_mutex_lock(&(coder->sim->state_mutex));
		coder->last_compile_start = ft_now();
		pthread_mutex_unlock(&(coder->sim->state_mutex));
		ft_log(coder, "is compiling");
		if (!ft_thread_wait(coder, coder->last_compile_start,
				coder->sim->config.time_to_compile, NULL))
		{
			pthread_mutex_lock(&(coder->sim->state_mutex));
			coder->compilations += 1;
			pthread_mutex_unlock(&(coder->sim->state_mutex));
		}
		ft_release_dongles(coder);
	}
	return (1);
}
