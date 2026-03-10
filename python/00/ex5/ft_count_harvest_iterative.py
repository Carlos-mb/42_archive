#!/usr/bin/env python3

def ft_count_harvest_iterative():
    days: int = int(input("Days until harvest: "))
    for i in range(1, days + 1):
        print(f"Day {i}")
    print("Harvest time!")
ft_count_harvest_iterative()