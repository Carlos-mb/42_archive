#!/usr/bin/env python3

def ft_count_harvest_recursive(total: int = 0, cont: int = 0) -> None:
    if cont == 0:
        ft_count_harvest_recursive(int(input("Days until harvest: ")), 1)
        return
    else:
        if total >= cont:
            print(f"Day {cont}")
            ft_count_harvest_recursive(total, cont + 1)
        if total < cont:
            print("Harvest time!")
ft_count_harvest_recursive()