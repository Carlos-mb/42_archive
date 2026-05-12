/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion_parse_config.c                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/04 11:19:10 by cmelero-          #+#    #+#             */
/*   Updated: 2026/05/05 18:26:45 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	parse_scheduler(char *str, char *scheduler)
{
	if (ft_strcmp(str, "fifo") == 0)
	{
		*scheduler = 'F';
		return (1);
	}
	if (ft_strcmp(str, "edf") == 0)
	{
		*scheduler = 'E';
		return (1);
	}
	return (0);
}

static int	ft_arg_debug(int argc, char **argv, t_simulation *sim)
{
	sim->config.debug = 0;
	if (argc == 10)
	{
		if (ft_strcmp(argv[9], "debug") == 0)
			sim->config.debug = 1;
		else
		{
			printf("Error: invalid debug argument.\n");
			return (0);
		}
	}
	return (1);
}

int	parse_config(t_simulation *sim, char **argv, int argc)
{
	if (!ft_arg_debug(argc, argv, sim))
		return (0);
	if (!ft_atoi_safe(argv[1], &sim->config.ncod) || sim->config.ncod <= 0)
		return (printf("Error: invalid number_of_coders\n"), 0);
	if (!ft_atoi_safe(argv[2], &sim->config.time_to_burnout)
		|| sim->config.time_to_burnout <= 0)
		return (printf("Error: invalid time_to_burnout\n"), 0);
	if (!ft_atoi_safe(argv[3], &sim->config.time_to_compile)
		|| sim->config.time_to_compile <= 0)
		return (printf("Error: invalid time_to_compile\n"), 0);
	if (!ft_atoi_safe(argv[4], &sim->config.time_to_debug))
		return (printf("Error: invalid time_to_debug\n"), 0);
	if (!ft_atoi_safe(argv[5], &sim->config.time_to_refactor))
		return (printf("Error: invalid time_to_refactor\n"), 0);
	if (!ft_atoi_safe(argv[6], &sim->config.compiles_required)
		|| sim->config.compiles_required <= 0)
		return (printf("Error: invalid number_of_compiles_required\n"), 0);
	if (!ft_atoi_safe(argv[7], &sim->config.dongle_cooldown))
		return (printf("Error: invalid dongle_cooldown\n"), 0);
	if (!parse_scheduler(argv[8], &sim->config.scheduler))
		return (printf("Error: scheduler must be fifo or edf\n"), 0);
	return (1);
}
