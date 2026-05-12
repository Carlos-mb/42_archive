/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion_queues.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/05 11:02:07 by cmelero-          #+#    #+#             */
/*   Updated: 2026/05/05 18:29:44 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	ft_add_to_queue(t_dongle *dongle, t_coder *coder)
{
	pthread_mutex_lock(&dongle->mutex);
	if (dongle->waitlist[coder->id - 1] == 0)
	{
		pthread_mutex_unlock(&dongle->mutex);
		if (dongle->sim->config.debug)
			ft_log(coder, "adding coder to waitlist of dongle");
		pthread_mutex_lock(&dongle->mutex);
		dongle->waitlist[coder->id - 1] = ft_now();
	}
	pthread_mutex_unlock(&dongle->mutex);
}

/* mutex already locked in ft_is_available */
static int	ft_first_in_fifo(t_dongle *dongle, t_coder *coder)
{
	int	i;
	int	out;

	i = 0;
	out = 1;
	while (out && i < coder->sim->config.ncod)
	{
		if (i != coder->id -1)
		{
			if (dongle->waitlist[i] != 0)
			{
				if (dongle->waitlist[coder->id -1] == 0)
					out = 0;
				else
				{
					if (dongle->waitlist[i] < dongle->waitlist[coder->id -1])
						out = 0;
				}
			}
		}
		i++;
	}
	return (out);
}

static int	ft_first_in_edf(t_dongle *dongle, t_coder *coder)
{
	int	i;
	int	out;

	i = 0;
	out = 1;
	while (out && i < coder->sim->config.ncod)
	{
		pthread_mutex_lock(&(dongle->sim->state_mutex));
		if (dongle->waitlist[i] != 0
			&& dongle->sim->coders[i].last_compile_start
			< dongle->sim->coders[coder->id -1].last_compile_start)
			out = 0;
		pthread_mutex_unlock(&(dongle->sim->state_mutex));
		i++;
	}
	return (out);
}

static int	ft_first_in_queue(t_dongle *dongle, t_coder *coder)
{
	if (coder->sim->config.scheduler == 'F')
		return (ft_first_in_fifo(dongle, coder));
	if (coder->sim->config.scheduler == 'E')
		return (ft_first_in_edf(dongle, coder));
	return (0);
}

int	ft_is_available(t_dongle *dongle, t_coder *coder)
{
	int	out;

	if (coder->sim->config.debug)
		ft_log(coder, "asks for dongle");
	pthread_mutex_lock(&(dongle->mutex));
	if (dongle->available && ft_now() >= dongle->cooldown_until_ms)
	{
		if (ft_first_in_queue(dongle, coder))
			out = 1;
		else
			out = 0;
	}
	else
	{
		out = 0;
		pthread_mutex_unlock(&(dongle->mutex));
		ft_add_to_queue(dongle, coder);
		pthread_mutex_lock(&(dongle->mutex));
	}
	pthread_mutex_unlock(&(dongle->mutex));
	if (coder->sim->config.debug)
		if (!(out == 1 && ft_log(coder, "dongle is available")))
			ft_log(coder, "dongle NOT available");
	return (out);
}
