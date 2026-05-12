/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_dongle_setup.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/03 18:50:00 by cmelero-          #+#    #+#             */
/*   Updated: 2026/05/05 15:30:43 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	ft_init_waitlists(t_simulation *sim, int i)
{
	int	j;

	j = 0;
	sim->dongles[i].waitlist = malloc(sizeof(long long) * sim->config.ncod);
	if (!sim->dongles[i].waitlist)
	{
		while (--i >= 0)
		{
			free(sim->dongles[i].waitlist);
			sim->dongles[i].waitlist = NULL;
		}
		return (0);
	}
	while (j < sim->config.ncod)
	{
		(sim->dongles[i].waitlist)[j] = 0;
		j++;
	}
	return (1);
}

int	ft_init_dongles(t_simulation *sim, int coders)
{
	int	i;

	sim->dongles = malloc(sizeof(t_dongle) * coders);
	if (sim->dongles == NULL)
		return (0);
	i = 0;
	while (i < coders)
	{
		sim->dongles[i].id = i;
		sim->dongles[i].available = 1;
		sim->dongles[i].cooldown_until_ms = 0;
		sim->dongles[i].sim = sim;
		if (!ft_init_waitlists(sim, i)
			|| (pthread_mutex_init(&sim->dongles[i].mutex, NULL) != 0))
		{
			while (--i >= 0)
				pthread_mutex_destroy(&sim->dongles[i].mutex);
			free(sim->dongles);
			sim->dongles = NULL;
			return (0);
		}
		i++;
	}
	return (1);
}

void	ft_free_mutex(t_simulation *sim)
{
	int	i;

	i = sim->config.ncod;
	while (--i >= 0)
	{
		pthread_mutex_destroy(&sim->dongles[i].mutex);
		pthread_mutex_destroy(&sim->coders[i].mutex);
		free(sim->dongles[i].waitlist);
	}
	free(sim->dongles);
	sim->dongles = NULL;
}
