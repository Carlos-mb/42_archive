/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_dongle_functions.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/02 11:53:59 by cmelero-          #+#    #+#             */
/*   Updated: 2026/05/05 13:54:02 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	ft_take_dongle(t_coder *coder, t_dongle *dongle)
{
	int	out;

	if (coder->sim->config.debug)
		ft_log(coder, "try to get dongle");
	out = 0;
	pthread_mutex_lock(&(dongle->mutex));
	if (ft_now() >= dongle->cooldown_until_ms)
	{
		if (dongle->available)
		{
			dongle->available = 0;
			out = 1;
			dongle->waitlist[coder->id - 1] = 0;
		}
	}
	pthread_mutex_unlock(&(dongle->mutex));
	if (out)
		ft_log(coder, "has taken a dongle");
	return (out);
}

int	ft_release_dongle(t_dongle *dongle, t_coder *coder)
{
	pthread_mutex_lock(&(dongle->mutex));
	dongle->available = 1;
	dongle->cooldown_until_ms = ft_now() + dongle->sim->config.dongle_cooldown;
	pthread_mutex_unlock(&(dongle->mutex));
	pthread_mutex_lock(&(dongle->sim->cond_mutex));
	pthread_cond_broadcast(&(dongle->sim->cond));
	pthread_mutex_unlock(&(dongle->sim->cond_mutex));
	if (coder->sim->config.debug)
		ft_log(coder, "has released a dongle");
	return (1);
}

int	ft_release_dongles(t_coder *coder)
{
	ft_release_dongle(coder->ld, coder);
	ft_release_dongle(coder->rd, coder);
	return (1);
}

int	ft_take_dongles(t_coder *coder)
{
	int	out;
	int	avail;

	avail = ft_is_available(coder->ld, coder);
	avail += ft_is_available(coder->rd, coder);
	out = 0;
	if (avail >= 2 && coder->ld != coder->rd)
	{
		if (ft_take_dongle(coder, coder->ld))
		{
			if (ft_take_dongle(coder, coder->rd))
				out = 1;
			else
			{
				ft_release_dongle(coder->ld, coder);
				ft_add_to_queue(coder->ld, coder);
			}
		}
	}
	return (out);
}
