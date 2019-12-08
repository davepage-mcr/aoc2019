#!/usr/bin/python3

import argparse
import pprint

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="Print out each instruction as executed", action="store_true")
parser.add_argument("filename", help="program source")
parser.add_argument("width", help="width in pixels", type=int)
parser.add_argument("height", help="height in pixels", type=int)
args = parser.parse_args()

pp = pprint.PrettyPrinter(indent=4)

inputfile = open(args.filename)
pixels = [int(x) for x in inputfile.readlines()[0].rstrip()]

# We need to turn this into a three dimensional array - layers x width x height
# We don't know how many layers there are yet!

pos = 0
minzeros = None
output = None

while pos < len(pixels):
    layerpx = []
    for i in range(args.height):
        line = pixels[pos:pos+args.width]
        pos += args.width
        layerpx += line
    zeros = len([x for x in layerpx if x == 0])
    ones  = len([x for x in layerpx if x == 1])
    twos  = len([x for x in layerpx if x == 2])

    if ( minzeros is None or zeros < minzeros ):
        if ( args.verbose ):
            print("New minimum zeros:", zeros, "on layer", i)
        output = ones * twos
        minzeros = zeros

print(output)
