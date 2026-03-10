#!/usr/bin/env python3

def ft_water_reminder():
    since: int = int(input("Days since last watering: "))
    if since > 2:
        print("Water the plants!")
    else:
        print("Plants are fine")
ft_water_reminder()