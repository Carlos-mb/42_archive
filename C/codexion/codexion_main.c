/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion_main.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/03 18:50:00 by cmelero-          #+#    #+#             */
/*   Updated: 2026/05/05 18:27:24 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	main(int argc, char **argv)
{
	t_simulation	sim;

	if (argc != 9)
	{
		printf("Error: wrong number of arguments\n");
		printf("cdrs burnout tto_cmp tto_deb tto_ref #compl cooldn fifo/edf\n");
		return (1);
	}
	if (!parse_config(&sim, argv, argc))
		return (1);
	if (!ft_init_simulation(&sim))
	{
		printf("Init error\n");
		return (1);
	}
	if (!ft_start_simulation(&sim))
		printf("ERROR creating threads. Waitting to created threads to end...");
	ft_run_simulation(&sim);
	ft_free_simulation(&sim);
	return (0);
}
