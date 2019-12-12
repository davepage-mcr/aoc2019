#!/usr/bin/python3

import argparse
import re

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="More output", action="store_true")
parser.add_argument("--steps", help="Target number of steps", type=int)
parser.add_argument("filename", help="Star Map")
args = parser.parse_args()

class Moon:
    def __init__(self, x, y, z):
        self.p = [x,y,z]
        self.v = [0,0,0]

    def step(self):
        for axis in range(3):
            self.p[axis] += self.v[axis]

    def energy(self):
        potential = 0
        kinetic = 0
        for axis in range(3):
            potential += abs(self.p[axis])
            kinetic   += abs(self.v[axis])
        return potential * kinetic

def invcmp(a, b):
    return (a < b) - (a > b)

# Turn our input file into a set of (x,y) tuples
inputfile = open(args.filename)
moons = set()
for line in inputfile:
    m = re.match('<x=(-?\d+), y=(-?\d+), z=(-?\d+)>', line)
    if m is None:
        print("Failed to match line:", line)
        exit(1)
    moon = Moon( int(m.group(1)), int(m.group(2)), int(m.group(3)) )
    moons.add(moon)

for steps in range(1, args.steps+1):
    # Calculate the acceleration due to gravity for each of our moons
    for moon in moons:
        for other in moons:
            if args.verbose:
                print("\tConsidering effect on our moon at", moon.p, "of other moon at", other.p)
            for axis in range(3):
                moon.v[axis] += invcmp(moon.p[axis], other.p[axis])

    for moon in moons:
        moon.step()

print("After", steps, "steps:")
totalenergy = 0
for moon in moons:
    energy = moon.energy()
    print("Moon at", moon.p, "has energy", energy)
    totalenergy += energy

print("Total energy:", totalenergy)
