#!/usr/bin/python3

import argparse
import pprint
import numpy

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

image = numpy.full((args.height, args.width), -1, dtype=int)

while pos < len(pixels):
    for y in range(args.height):
        line = pixels[pos:pos+args.width]
        for x in range(len(line)):
            if image[y][x] == -1 and line[x] != 2:
                image[y][x] = line[x]

        pos += args.width

for line in image:
    print( ''.join([str(x) for x in line]) )
