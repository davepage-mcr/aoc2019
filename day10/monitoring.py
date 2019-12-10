#!/usr/bin/python3

import argparse
import numpy

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="Print out each instruction as executed", action="store_true")
parser.add_argument("filename", help="Star Map")
args = parser.parse_args()

def smallestvector( x, y ):
    biggestfactor = max(abs(x), abs(y))
    for i in range(2,biggestfactor+1):
        while( x % i == 0 and y % i == 0 ):
            x //= i
            y //= i
    return (x, y)

def visiblefrom(prospect, target):
    vector = ( target[0]-prospect[0], target[1]-prospect[1] )
    if args.verbose:
        print("Testing whether", prospect, "can see", target, "at vector", vector)
    # Now find the smallest fraction of the vector which is still an integer
    step = smallestvector( vector[0], vector[1] )
    if step == vector:
        if args.verbose:
            print("\tOne integer step to target, so we can see it")
        return True

    if args.verbose:
        print("\tStepping", step, "from", prospect)
    x = prospect[0]
    y = prospect[1]

    while True:
        x += step[0]
        y += step[1]
    
        if x == target[0] and y == target[1]:
            if args.verbose:
                print("\tNothing in the way by stepping", step)
            return True

        if ( x, y ) in asteroids:
            if args.verbose:
                print("\tHit asteroid at", (x,y), "on way to", target)
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
