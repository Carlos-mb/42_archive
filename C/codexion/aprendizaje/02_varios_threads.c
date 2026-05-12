/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   02_varios_threads.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/02 10:28:56 by cmelero-          #+#    #+#             */
/*   Updated: 2026/05/02 14:11:30 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	*ft_thread_test(void *coder)
{
	printf("Coder %d thread is running\n", (*(coder_t *)coder).id);
//	printf("Coder %d thread is running\n", ((coder_t *) coder)->id);
	return (NULL);
}

int	main(void)
{
	pthread_t	*threads;
	coder_t		*coders;

	// RECUERDA: este código es para apender threads, no estoy manejando errores adecuadamente

	threads = malloc(sizeof(pthread_t) * 3);
	coders = malloc(sizeof(coder_t) * 3);

	for (int i=0; i <3; i++)
	{
		(coders[i]).id = i+1;
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
	printf("Main ends\n");
	return (0);
}
