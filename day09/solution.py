#!/usr/bin/python3

import sys
sys.path.append("../lib")

import argparse
from itertools import permutations
import numpy
import intcode

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="Print out each instruction as executed", action="store_true")
parser.add_argument("--decode", help="Print out argument decoding", action="store_true")
parser.add_argument("filename", help="program source")
parser.add_argument("input", help="input data", nargs="*", type=int)
args = parser.parse_args()

inputfile = open(args.filename)
for line in inputfile:
    program = [int(x) for x in line.split(',')]

    computer = intcode.IntCode(program.copy(), args)
    output = computer.compute(args.input)

    print("Output:", output)
