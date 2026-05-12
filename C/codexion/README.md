*This project has been created as part of the 42 curriculum by cmelero-.*

# Codexion

## Description

Codexion is a multithreaded C simulation of coders competing for shared dongles.

Each coder is represented by one thread. A coder needs two dongles to compile. After compiling, the coder debugs and refactors before trying to compile again.

The simulation ends when one coder burns out or when all coders have completed the required number of compilations.

The project implements synchronization with pthreads, mutexes and a condition variable.

## Instructions

Build the project with:

    make

Run the program with:

    ./codexion number_of_coders time_to_burnout time_to_compile time_to_debug time_to_refactor number_of_compiles_required dongle_cooldown scheduler

Example:

    ./codexion 3 800 200 200 200 2 0 fifo

If your local Makefile builds `codexion.exe`, use:

    ./codexion 3 800 200 200 200 2 0 fifo

Arguments:

- `number_of_coders`: number of coder threads.
- `time_to_burnout`: maximum time in milliseconds before a coder burns out.
- `time_to_compile`: time in milliseconds spent compiling.
- `time_to_debug`: time in milliseconds spent debugging.
- `time_to_refactor`: time in milliseconds spent refactoring.
- `number_of_compiles_required`: number of completed compilations required per coder.
- `dongle_cooldown`: time in milliseconds before a released dongle can be reused.
- `scheduler`: scheduling policy.

Subject scheduler values:

- `fifo`
- `edf`

Normal output format:

    timestamp coder_id has taken a dongle
    timestamp coder_id is compiling
    timestamp coder_id is debugging
    timestamp coder_id is refactoring
    timestamp coder_id burned out

Timestamps are printed in milliseconds from the start of the simulation.

Use valgrind --tool=helgrind to check data races

## Resources

The implementation uses:

- `pthread_create` and `pthread_join` for coder and monitor threads.
- `pthread_mutex_t` to protect shared state, dongles and logging.
- `pthread_cond_t` to wake coders when shared resource state may have changed.
- `gettimeofday` to compute millisecond timestamps.
- a Makefile compiled with `-Wall -Wextra -Werror -pthread`.

No standard library priority queue is used.

## Blocking cases handled

The program handles these blocking or terminal cases:

- invalid argument count;
- invalid numeric arguments;
- invalid scheduler value;
- one coder with one dongle;
- coder burnout;
- all coders completing the required number of compilations;
- dongle cooldown after release;
- coders waiting for unavailable dongles;
- global wakeup when the simulation stops.

## Thread synchronization mechanisms

The simulation uses several synchronization mechanisms:

- `log_mutex` serializes output so log lines do not overlap.
- `state_mutex` protects shared simulation state such as `stop_now`, `compilations` and `last_compile_start`.
- each dongle has its own mutex to protect `available`, `cooldown_until_ms` and waitlist state.
- `cond_mutex` and `cond` are used to wake coder threads when dongle availability, cooldown or simulation stop state may have changed.
- the monitor thread checks burnout and completion conditions and stops the simulation when required.

FIFO scheduling selects the coder that requested a dongle first.

EDF scheduling selects the coder closest to burnout, based on the oldest `last_compile_start`.

## AI usage

AI assistance was used during development as a learning and review tool.

It helped with:

- understanding pthreads;
- reviewing possible race conditions;
- planning tests;
- drafting documentation.

All final code decisions, implementation choices and project responsibility belong to cmelero-.
