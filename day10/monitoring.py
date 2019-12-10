#!/usr/bin/python3

import argparse
import numpy
import math

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="Print out each instruction as executed", action="store_true")
parser.add_argument("--part2", help="Activate the GIANT LASER", action="store_true")
parser.add_argument("filename", help="Star Map")
args = parser.parse_args()

def getangle(laser, target):
    vector = ( target[0]-laser[0], target[1]-laser[1] )

    # reverse the y coordinates!
    return math.degrees( math.atan2( target[0]-laser[0], laser[1]-target[1] ) ) % 360

def smallestvector( x, y ):
    biggestfactor = max(abs(x), abs(y))
    for i in range(2,biggestfactor+1):
        while( x % i == 0 and y % i == 0 ):
            x //= i
            y //= i
    return (x, y)

def visiblefrom(prospect, target):
    vector = ( target[0]-prospect[0], target[1]-prospect[1] )
    # Now find the smallest fraction of the vector which is still an integer
    step = smallestvector( vector[0], vector[1] )
    if step == vector:
        return True

    x = prospect[0]
    y = prospect[1]

    while True:
        x += step[0]
        y += step[1]
    
        if x == target[0] and y == target[1]:
            return True

        if ( x, y ) in asteroids:
            return False


# Turn our input file into a set of (x,y) tuples
inputfile = open(args.filename)
linenum = 0
asteroids = set()
for line in inputfile:
    for i in range(len(line)):
        if line[i] == '#':
            asteroids.add( (i,linenum) )
    linenum += 1

max_x = i
max_y = linenum

max_prospect = None
max_visible = 0

# Now see which of these can see each other
for prospect in asteroids:
    visibletargets = 0
    for target in asteroids:
        if prospect == target:
            # Skip ourselves obviously
            continue
        if visiblefrom(prospect, target):
            visibletargets += 1

    if args.verbose: 
        print(prospect, "can see", visibletargets, "asteroids")

    if visibletargets > max_visible:
        max_visible = visibletargets
        max_prospect = prospect

print("Best prospect is", max_prospect, "which can see", max_visible, "asteroids")

if not args.part2:
    exit(0)

# Now it's giant death laser time!
print("Firing up the giant death laser!")

laser = max_prospect

victim = 1
while len(asteroids) > 1:
    visible_asteroids = {}              # dict of (coordinates) => angle, we can sort by angle later
    for target in asteroids:
        # Iterate over the asteroids, see which ones we can see, and what angle they're at from us
        if target == laser:
            # Do not vaporise ourselves!
            continue
        if visiblefrom(laser, target):
            visible_asteroids[target] = getangle(laser, target)

    visible_by_angle = sorted(visible_asteroids, key=visible_asteroids.__getitem__)

    for target in visible_by_angle:
        print(target,"at", visible_asteroids[target], "is victim number", victim)
        asteroids.remove(target)

        victim += 1

    print("Next round?")
