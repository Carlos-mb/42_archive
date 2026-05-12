/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: cmelero- <cmelero-@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/02 10:56:26 by cmelero-          #+#    #+#             */
/*   Updated: 2026/05/12 08:32:40 by cmelero-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef CODEXION_H
# define CODEXION_H

# include <stdbool.h>
# include <stdio.h>
# include <sys/time.h>
# include <unistd.h>
# include <pthread.h>
# include <stdlib.h>

# define SLEEP 100

typedef struct s_coder		t_coder;
typedef struct s_simulation	t_simulation;

typedef struct s_config
{
	int		ncod;
	int		time_to_burnout;
	int		time_to_compile;
	int		time_to_debug;
	int		time_to_refactor;
	int		compiles_required;
	int		dongle_cooldown;
	char	scheduler;
	char	debug;
}	t_config;

typedef struct s_dongle
{
	int				id;
	char			available;
	long long		cooldown_until_ms;
	long long		*waitlist;
	t_simulation	*sim;
	pthread_mutex_t	mutex;
}	t_dongle;

typedef struct s_coder
{
	int				id;
	int				compilations;
	long long		last_compile_start;
	t_dongle		*ld;
	t_dongle		*rd;
	t_simulation	*sim;
	pthread_t		thread;
	char			burned;
	char			ended;
	pthread_mutex_t	mutex;
}	t_coder;

typedef struct s_simulation
{
	pthread_mutex_t	log_mutex;
	pthread_mutex_t	state_mutex;
	pthread_t		monitor_thread;
	long long		started;
	t_dongle		*dongles;
	t_coder			*coders;
	t_config		config;
	char			stop_now;
	pthread_cond_t	cond;
	pthread_mutex_t	cond_mutex;
}	t_simulation;

long long	ft_now(void);
long long	ft_ms(struct timeval tv);
int			ft_take_dongle(t_coder *coder, t_dongle *dongle);
int			ft_release_dongle(t_dongle *dongle, t_coder *coder);
int			ft_release_dongles(t_coder *coder);
int			ft_is_available(t_dongle *dongle, t_coder *coder);
int			ft_take_dongles(t_coder *coder);
int			ft_init_dongles(t_simulation *sim, int coders);
void		ft_free_mutex(t_simulation *sim);
char		ft_stop_read(t_simulation *sim);
void		ft_log_burned(t_coder *coder, const char *string);
int			ft_log(t_coder *coder, const char *string);
int			ft_read_compilations(t_coder *coder);
void		ft_stop(t_simulation *sim);
void		*ft_thread_monitor(void *sim_in);
void		*ft_thread_coder(void *coder_in);
int			ft_init_simulation(t_simulation *sim);
void		ft_free_simulation(t_simulation *sim);
int			ft_start_threads(t_simulation *sim);
int			ft_start_simulation(t_simulation *sim);
int			ft_run_simulation(t_simulation *sim);
void		*ft_thread_monitor_impl(t_simulation *sim);
void		*ft_thread_coder_impl(t_coder *coder);
int			ft_init_simulation_impl(t_simulation *sim);
int			parse_config(t_simulation *sim, char **argv, int argc);
void		ft_add_to_queue(t_dongle *dongle, t_coder *coder);
int			ft_init_waitlists(t_simulation *sim, int i);
void		ft_wakeup(t_simulation *sim);
int			ft_actived_coders(t_simulation *sim);
void		ft_thread_monitor_scan(t_simulation *sim, int *compled, char *stop);
void		ft_dongle_monitor_scan(t_simulation *sim);
int			ft_compile_cycle(t_coder *coder);
char		ft_thread_wait(t_coder *coder, long long time, long long pause,
				const char *string);
int			ft_strcmp(char *s1, char *s2);
int			ft_is_number(char *str);
int			ft_atoi_safe(char *str, int *result);

#endif
