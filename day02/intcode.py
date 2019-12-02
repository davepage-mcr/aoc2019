#!/usr/bin/python3

import argparse

def do_add(program, pos):
    # The opcode at pos is add (1)
    pos_a = program[pos+1]
    pos_b = program[pos+2]
    pos_t = program[pos+3]
    if args.verbose:
        print(pos, "add opcode: Sum values at", pos_a, pos_b, "into", pos_t)
    program[pos_t] = program[pos_a] + program[pos_b]

def do_mult(program, pos):
    # The opcode at pos is mult (1)
    pos_a = program[pos+1]
    pos_b = program[pos+2]
    pos_t = program[pos+3]
    if args.verbose:
        print(pos, "mult opcode: Multiply values at", pos_a, pos_b, "into", pos_t)
    program[pos_t] = program[pos_a] * program[pos_b]

def compute(program):
    if args.verbose:
        print("### New program", program)
    pos=0
    while(1):
        if args.verbose:
            print("# Looking for opcode at", pos)
        opcode = program[pos]
        if opcode == 99:
            return
        elif opcode == 1:
            do_add(program, pos)
        elif opcode == 2:
            do_mult(program, pos)
        else:
            print("Unrecognised opcode", opcode, "at position", pos)
            print(program)
            exit(1)
        pos += 4

def search(masterprogram, target):
    # Brute-force program until we end up with target in program[0]
    for noun in range(0,99+1):
        for verb in range(0,99+1):
            program = masterprogram.copy()
            program[1] = noun
            program[2] = verb

            compute(program)

            if program[0] == target:
                print("Reached target with noun", noun, "verb", verb)
                return

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--debug", help="Apply 1202 program alarm debugging", action="store_true")
parser.add_argument("--verbose", help="Print out each instruction as executed", action="store_true")
parser.add_argument("--target", help="Search for noun and verb which produce this output", type=int)
parser.add_argument("filename", help="program input")
args = parser.parse_args()

inputfile = open(args.filename)
for line in inputfile:
    program = [int(x) for x in line.split(',')]

    if args.target:
        print("Searching for a target of", args.target)
        search(program, args.target)
        exit(0)

    if args.debug:
        program[1]=12
        program[2]=2

    compute(program)
    print("Final state:", program)
