#!/usr/bin/python3

import argparse
import pprint

pp = pprint.PrettyPrinter()

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--distance", help="Find shortest wire distance crossover, not closest manhattan distance", action="store_true")
parser.add_argument("filename", help="program input")
args = parser.parse_args()

wires=[]

def manhattan (coords):
    return abs(coords[0])+abs(coords[1])

def process ( instructions ):
    wirecoords = set()
    wiredist = {}

    x = 0
    y = 0
    dist = 0

    for instruction in instructions:
        direction = instruction[0]
        magnitude = int(instruction[1:])

        for i in range(magnitude):
            dist += 1
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

            if ( x, y ) not in wiredist:
                wiredist[ (x,y) ] = dist
            wirecoords.add( (x,y) )

    if ( args.distance ):
        return wiredist
    else:
        return wirecoords

inputfile = open(args.filename)
for line in inputfile:
    instructions = line.split(',')
    wires.append( process(instructions) )

if ( args.distance ):
    # Get the intersection of the dict keys
    firstkeys = set( wires[0].keys() )
    secondkeys = set( wires[1].keys() )
    crossovers = firstkeys.intersection(secondkeys)

    # Get the wire length distance for each crossover
    distances = [ wires[0][i] + wires[1][i] for i in crossovers ]

else:
    # Crossovers are intersections between these wires
    crossovers = wires[0].intersection(wires[1])

    # Get the Manhattan distance of each crossover
    distances = [ manhattan(i) for i in crossovers ]

mindistance = min(distances)
print("Closest crossover is at", mindistance)
