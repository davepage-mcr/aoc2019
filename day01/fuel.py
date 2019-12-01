#!/usr/bin/python3

import fileinput

def getfuel(mass):
    fuel = int(mass/3)-2
    return(fuel)

totalfuel=0

for line in fileinput.input():
    mass = int(line)
    fuel = getfuel(mass)
    print("Module weighs", mass, "needs", fuel)
    totalfuel += fuel

print("Total fuel requirement:", totalfuel)
