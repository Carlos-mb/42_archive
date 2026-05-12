/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   03_bloqueos_con_mutex.c                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/02 10:28:56 by cmelero-          #+#    #+#             */
/*   Updated: 2026/05/02 15:19:06 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	*ft_thread_test(void *coder_in)
{
	t_coder	*coder;

	coder = (t_coder *)coder_in;

// pthread_mutex_lock()
//     espera hasta poder bloquear el mutex

// pthread_mutex_trylock()
//     intenta bloquearlo inmediatamente
//     si está ocupado, no espera

	if (pthread_mutex_lock(&(coder->simulation->log_mutex)) == 0)
	{
		printf("Coder %d thread is running\n", coder->id);
		pthread_mutex_unlock(&(coder->simulation->log_mutex));
	}
	return (NULL);
}

int	ft_init_simulation(t_simulation *simulation)
{
	int	out;

	out = pthread_mutex_init(&(simulation -> log_mutex), NULL) == 0;

	return (out);
}


int	main(void)
{
	pthread_t		*threads;
	t_coder			*coders;
	t_simulation	simulation;

	if (!ft_init_simulation(&simulation))
	{
		printf("Init error\n");
		return (1);
	}

	threads = malloc(sizeof(pthread_t) * 3);
	coders = malloc(sizeof(t_coder) * 3);

	for (int i=0; i <3; i++)
	{
		(coders[i]).id = i + 1;
		// (coders + i)->id = i + 1;
		(coders[i]).simulation = &simulation;
	}
	printf("Main starts\n");

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
	printf("Main ends\n");
	return (0);
}
