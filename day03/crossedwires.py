#!/usr/bin/python3

import argparse
import pprint

pp = pprint.PrettyPrinter()

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("filename", help="program input")
args = parser.parse_args()

wires=[]

def manhattan (coords):
    return abs(coords[0])+abs(coords[1])

def process ( instructions ):
   # Return a set of co-ordinate tuples, not including the origin
   wire = set()
   x = 0
   y = 0

   for instruction in instructions:
        direction = instruction[0]
        magnitude = int(instruction[1:])

        for i in range(magnitude):
            if( direction == 'U' ):
                y += 1
            elif( direction == 'D' ):
                y -= 1
            elif( direction == 'L' ):
                x -= 1
            elif( direction == 'R' ):
                x += 1
            else:
                print("Unknown direction", direction)
                exit(1)
            wire.add( (x,y) )

   return wire

inputfile = open(args.filename)
for line in inputfile:
    instructions = line.split(',')
    wires.append( process(instructions) )

# Crossovers are intersections between these wires
crossovers = wires[0].intersection(wires[1])

# Get the lowest Manhattan distance of these
distances = [ manhattan(x) for x in crossovers ]
mindistance = min(distances)

print("Closest crossover is at", mindistance)
