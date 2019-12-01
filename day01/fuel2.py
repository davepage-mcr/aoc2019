#!/usr/bin/python3

import fileinput

def getfuel(mass):
    fuel = int(mass/3)-2
    if fuel < 0:
        fuel=0
    return(fuel)

def getfuel2(mass):
    totfuel = 0
    while getfuel(mass) > 0:
        fuel = getfuel(mass)
        # print("Mass", mass, "needs", fuel)
        totfuel += fuel
        mass=fuel
    print("Module and fuel needs", totfuel)
    return(totfuel)

totalfuel=0

for line in fileinput.input():
    mass = int(line)
    fuel = getfuel2(mass)
    totalfuel += fuel

print("Total fuel requirement:", totalfuel)
