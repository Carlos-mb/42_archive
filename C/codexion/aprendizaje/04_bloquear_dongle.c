/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   04_bloquear_dongle.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/02 10:28:56 by cmelero-          #+#    #+#             */
/*   Updated: 2026/05/02 18:04:43 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	ft_log(t_coder *coder, const char *string)
{
	if (pthread_mutex_lock(&(coder->simulation->log_mutex)) == 0)
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

void	*ft_thread_test(void *coder_in)
{
	t_coder	*coder;

	coder = (t_coder *)coder_in;
	ft_log(coder, "is running");
	ft_take_dongle(coder, coder->left_dongle);
	return (NULL);
}

int	ft_init_simulation(t_simulation *simulation)
{
	int	out;

	out = pthread_mutex_init(&(simulation -> log_mutex), NULL) == 0;
	return (out);
}

int	ft_start_simulation(t_simulation *simulation)
{
	simulation->started = ft_now();
	return (0);
}

int	main(void)
{
	pthread_t		*threads;
	t_coder			*coders;
	t_simulation	simulation;
	t_dongle		dongle;

	if (!ft_init_simulation(&simulation))
	{
		printf("Init error\n");
		return (1);
	}

	threads = malloc(sizeof(pthread_t) * 3);
	coders = malloc(sizeof(t_coder) * 3);

	dongle.available = 1;

	for (int i=0; i <3; i++)
	{
		(coders[i]).id = i + 1;
		// (coders + i)->id = i + 1;
		(coders[i]).simulation = &simulation;
		(coders[i]).left_dongle = &dongle;
	}
	printf("Main starts\n");
	pthread_mutex_init(&(dongle.mutex), NULL);
	ft_start_simulation(&simulation);
	for (int i=0; i<3; i++)
	{
		if (pthread_create(&(threads[i]), NULL, ft_thread_test, &(coders[i])) != 0)
		{
			printf("Error creating thread");
		}
	}
	for (int i=0; i<3; i++)
	{
		if (pthread_join(threads[i], NULL) != 0)
		{
			printf("Error joining\n");
		}
	}

	free(coders);
	free(threads);
	pthread_mutex_destroy(&(simulation.log_mutex));
	pthread_mutex_destroy(&(dongle.mutex));
	printf("Main ends\n");

	return (0);
}
