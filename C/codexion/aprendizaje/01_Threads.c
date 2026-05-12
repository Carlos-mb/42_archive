/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   01_Threads.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/02 10:28:56 by cmelero-          #+#    #+#             */
/*   Updated: 2026/05/02 13:18:41 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	*ft_thread_test(void *coder_id)
{
	printf("Coder %d thread is running\n", *(int *)coder_id);
	return (NULL);
}

int	main(void)
{
	pthread_t	thread;
	int			coder_id = 1;

	printf("Main starts\n");
	if (pthread_create(&thread, NULL, ft_thread_test, &coder_id) != 0)
	{
		printf("Error creating thread");
		return (1);
	}

	// join -> lánzalo y espera a que termine. Si no espero, main podría
	// terminar antes de que termine la función
	if (pthread_join(thread, NULL) != 0)
	{
		printf("Error joining\n");
		return (1);
	}
	printf("Main ends\n");
	return (0);
}
