/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   05_pelea_por_dongles.c                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/02 10:28:56 by cmelero-          #+#    #+#             */
/*   Updated: 2026/05/02 19:45:32 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	ft_log(t_coder *coder, const char *string)
{
	if (pthread_mutex_lock(&((coder->simulation)->log_mutex)) == 0)
	{
		printf("%lld %d %s\n",
			ft_now() - coder->simulation->started,
			coder->id,
			string);
		pthread_mutex_unlock(&(coder->simulation->log_mutex));
	}
}

int	ft_take_dongle(t_coder *coder, t_dongle *dongle)
{
	int	out;
	pthread_mutex_lock(&(dongle->mutex));
	if (dongle->available)
	{
		dongle->available = 0;
		out = 1;
	}
	else
	{
		out = 0;
	}
	pthread_mutex_unlock(&(dongle->mutex));
	if (out)
		ft_log(coder, "has taken a dongle");
	else
		ft_log(coder, "could not take dongle");
	return (out);
}


int	ft_release_dongle(t_coder *coder, t_dongle *dongle)
{
	pthread_mutex_lock(&(dongle->mutex));
	dongle->available = 1;
	pthread_mutex_unlock(&(dongle->mutex));
	ft_log(coder, "has released a dongle");
	return (1);
}

int	ft_take_dongles(t_coder *coder)
{
	int	out;

	out = 0;
	if (ft_take_dongle(coder, coder->left_dongle))
	{
		if (ft_take_dongle(coder, coder->right_dongle))
			out = 1;
		else
			ft_release_dongle(coder, coder->left_dongle);
	}
	return (out);
}

void	*ft_thread_test(void *coder_in)
{
	t_coder	*coder;

	coder = (t_coder *)coder_in;
	ft_log(coder, "is running");
	ft_take_dongle(coder, coder->left_dongle);
	ft_take_dongle(coder, coder->right_dongle);
	return (NULL);
}

int	ft_init_dongles(t_simulation *simulation, int coders)
{
	int	i;

	if (coders <= 0)
		return (0);
	simulation->dongles = malloc(sizeof(t_dongle) * coders);
	if (simulation->dongles == NULL)
		return (0);
	i = 0;
	while (i < coders)
	{
		simulation->dongles[i].id = i;
		simulation->dongles[i].available = 1;
		simulation->dongles[i].cooldown_until_ms = 0;
		if (pthread_mutex_init(&simulation->dongles[i].mutex, NULL) != 0)
		{
			while (--i >= 0)
				pthread_mutex_destroy(&simulation->dongles[i].mutex);
			free(simulation->dongles);
			simulation->dongles = NULL;
			return (0);
		}
		i++;
	}
	return (1);
}

void	ft_free_dongles(t_simulation *simulation)
{
	int i;

	i = simulation->coder_count;
	while (--i >= 0)
		pthread_mutex_destroy(&simulation->dongles[i].mutex);
	free(simulation->dongles);
	simulation->dongles = NULL;
}

int	ft_init_simulation(t_simulation *simulation, int coders)
{
	int i;

	simulation->coders = malloc (sizeof(t_coder) * coders);
	if (!simulation->coders)
		return (0);
	if (pthread_mutex_init(&(simulation -> log_mutex), NULL) != 0)
	{
		free(simulation->coders);
		return (0);
	}
	if (!ft_init_dongles(simulation, coders))
	{
		pthread_mutex_destroy(&simulation->log_mutex);
		free(simulation->coders);
		return (0);
	}
	simulation->coder_count = coders;
	i = 0;
	while (i < coders)
	{
		simulation->coders[i].id = i + 1;
		simulation->coders[i].left_dongle = &(simulation->dongles[i]);
		simulation->coders[i].compilations = 0;
		simulation->coders[i].simulation = simulation;
		if (i == coders -1)
			simulation->coders[i].right_dongle = &(simulation->dongles[0]);
		else
			simulation->coders[i].right_dongle = &(simulation->dongles[i + 1]);
		i++;
	}
	return (1);
}

void	ft_free_simulation(t_simulation *simulation)
{
	pthread_mutex_destroy(&(simulation->log_mutex));
	ft_free_dongles(simulation);
	free(simulation->coders);
}

int	ft_start_simulation(t_simulation *simulation)
{
	simulation->started = ft_now();
	return (0);
}

int	main(void)
{
	pthread_t		*threads;
	t_simulation	simulation;
	int				coders_count = 3;

	threads = malloc(sizeof(pthread_t) * coders_count);
	if (!threads)
		return (1);
	if (!ft_init_simulation(&simulation, coders_count))
	{
		printf("Init error\n");
		return (1);
	}

	printf("Main starts\n");
	ft_start_simulation(&simulation);
	for (int i=0; i<coders_count; i++)
	{
		if (pthread_create(&(threads[i]), NULL, ft_thread_test, &(simulation.coders[i])) != 0)
		{
			printf("Error creating thread");
		}
	}
	for (int i=0; i<coders_count; i++)
	{
		if (pthread_join(threads[i], NULL) != 0)
		{
			printf("Error joining\n");
		}
	}

	free(threads);
	ft_free_simulation(&simulation);
	printf("Main ends\n");

	return (0);
}

/*
Ejemplo de salida:

Main starts
0 1 is running
0 1 has taken a dongle
0 1 has taken a dongle
0 3 is running
0 3 has taken a dongle
0 3 could not take dongle
0 2 is running
0 2 could not take dongle
0 2 could not take dongle
Main ends

*/
