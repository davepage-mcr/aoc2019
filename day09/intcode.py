#!/usr/bin/python3

import argparse
from itertools import permutations
import numpy

class IntCode:

    def __init__( self, program ):
        self.program = numpy.zeros( (100000), dtype=int)
        for i in range(len(program)):
            self.program[i] = program[i]
        self.pos = 0
        self.relbase = 0

    def decode_argument(self, argument, mode):
        if args.decode:
            print("\tDecoding argument", argument, "with mode", mode)

        if mode == 0:
            if args.decode:
                print("\tPosition mode;", argument, "is an address containing", self.program[argument])
            return( self.program[argument] )
        elif mode == 2:
            if args.decode:
                print("\tRelative base mode;", argument, "is an address containing", self.program[argument + self.relbase])
            return( self.program[argument + self.relbase] )
        elif mode == 1:
            if args.decode:
                print("\tImmediate mode;", argument, "is a value")
            return( argument ) 
        else:
            print("Unrecognised mode:", mode)
            exit(1)

    def do_add(self, modes):
        if args.verbose:
            print("\t", self.program[self.pos:self.pos+4])
        arg_a = self.decode_argument( self.program[self.pos+1], modes[0] )
        arg_b = self.decode_argument( self.program[self.pos+2], modes[1] )
        pos_t = self.program[self.pos+3]
        if args.verbose:
            print("\tSum values", arg_a, arg_b, "into", pos_t)
        self.program[pos_t] = arg_a + arg_b
        return( [0, 4] )

    def do_mult(self, modes):
        if args.verbose:
            print("\t", self.program[self.pos:self.pos+4])
        arg_a = self.decode_argument( self.program[self.pos+1], modes[0] )
        arg_b = self.decode_argument( self.program[self.pos+2], modes[1] )
        pos_t = self.program[self.pos+3]
        if args.verbose:
            print("\tMultiply values", arg_a, arg_b, "into", pos_t)
        self.program[pos_t] = arg_a * arg_b
        return( [0, 4] )

    def do_input(self):
        arg_a = self.program[self.pos+1]

        if len(self.inputdata) == 0:
            print("Want to receive input but we have none!")
            exit(1)

        value = self.inputdata.pop(0)
        if args.verbose:
            print("\tStoring input value", value, "at location", arg_a)
        self.program[arg_a] = value

        return( [0, 2] )

    def do_output(self, modes):
        if args.verbose:
            print("\t", self.program[self.pos:self.pos+2])
        arg_a = self.decode_argument( self.program[self.pos+1], modes[0] )

        self.output.append(arg_a)

        return( [0, 2] )

    def do_jit(self, modes):
        if args.verbose:
            print("\t", self.program[self.pos:self.pos+3])
        arg_a = self.decode_argument( self.program[self.pos+1], modes[0] )
        arg_b = self.decode_argument( self.program[self.pos+2], modes[1] )

        if arg_a != 0:
            if args.verbose:
                print("\t", arg_a, "is nonzero, jumping to", arg_b)
            return([1, arg_b])
        else:
            if args.verbose:
                print("\t", arg_a, "is zero, doing nothing")
            return([0, 3])

    def do_jif(self, modes):
        if args.verbose:
            print("\t", self.program[self.pos:self.pos+3])
        arg_a = self.decode_argument( self.program[self.pos+1], modes[0] )
        arg_b = self.decode_argument( self.program[self.pos+2], modes[1] )

        if arg_a == 0:
            if args.verbose:
                print("\t", arg_a, "is zero, jumping to", arg_b)
            return([1, arg_b])
        else:
            if args.verbose:
                print("\t", arg_a, "is nonzero, doing nothing")
            return([0, 3])

    def do_lt(self, modes):
        if args.verbose:
            print("\t", self.program[self.pos:self.pos+3])
        arg_a = self.decode_argument( self.program[self.pos+1], modes[0] )
        arg_b = self.decode_argument( self.program[self.pos+2], modes[1] )
        arg_c = self.program[self.pos+3]

        if arg_a < arg_b:
            if args.verbose:
                print("\t", arg_a, "is less than", arg_b, "; storing 1 at", arg_c)
            self.program[arg_c] = 1
        else:
            if args.verbose:
                print("\t", arg_a, "is not less than", arg_b, "; storing 0 at", arg_c)
            self.program[arg_c] = 0

        return([0, 4])

    def do_eq(self, modes):
        if args.verbose:
            print("\t", self.program[self.pos:self.pos+3])
        arg_a = self.decode_argument( self.program[self.pos+1], modes[0] )
        arg_b = self.decode_argument( self.program[self.pos+2], modes[1] )
        arg_c = self.program[self.pos+3]

        if arg_a == arg_b:
            if args.verbose:
                print("\t", arg_a, "is equal to", arg_b, "; storing 1 at", arg_c)
            self.program[arg_c] = 1
        else:
            if args.verbose:
                print("\t", arg_a, "is not equal to", arg_b, "; storing 0 at", arg_c)
            self.program[arg_c] = 0

        return([0, 4])

    def do_rbo(self, modes):
        if args.verbose:
            print("\t", self.program[self.pos:self.pos+2])
        arg_a = self.decode_argument( self.program[self.pos+1], modes[0] )
        self.relbase += arg_a

        return([0, 2])

    def compute(self, inputdata):
        self.pos=0
        self.inputdata = inputdata
        self.output = []

        while(1):
            if args.verbose:
                print("# Looking for opcode at", self.pos, ":", self.program[self.pos])

            opcode = self.program[self.pos] % 100
            modes = [ ( self.program[self.pos] // dec ) % 10 for dec in [ 100, 1000, 10000 ] ]

            if opcode == 99:
                return(self.output)
            elif opcode == 1:
                inst_len = self.do_add(modes)
            elif opcode == 2:
                inst_len = self.do_mult(modes)
            elif opcode == 3:
                inst_len = self.do_input()
            elif opcode == 4:
                inst_len = self.do_output(modes)
            elif opcode == 5:
                inst_len = self.do_jit(modes)
            elif opcode == 6:
                inst_len = self.do_jif(modes)
            elif opcode == 7:
                inst_len = self.do_lt(modes)
            elif opcode == 8:
                inst_len = self.do_eq(modes)
            elif opcode == 9:
                inst_len = self.do_rbo(modes)
            else:
                print("Unrecognised opcode", opcode, "at position", self.pos)
                print(self.program)
                exit(1)

            if inst_len[0] == 0:    # We've returned a relative jump for pos
                self.pos += inst_len[1]
            elif inst_len[0] == 1:  # Absolute position
                self.pos = inst_len[1]
            else:
                print("Unexpected return type", inst_len[0])
                exit(1)

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="Print out each instruction as executed", action="store_true")
parser.add_argument("--decode", help="Print out argument decoding", action="store_true")
parser.add_argument("filename", help="program source")
args = parser.parse_args()

inputfile = open(args.filename)
for line in inputfile:
    program = [int(x) for x in line.split(',')]

    computer = IntCode(program.copy())
    output = computer.compute([])

    print("Output:", output)
