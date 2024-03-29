#!/usr/bin/python3

import argparse

def decode_argument( program, argument, mode ):
    if args.decode:
        print("\tDecoding argument", argument, "with mode", mode)

    if mode == 0:
        if args.decode:
            print("\tPosition mode;", argument, "is an address containing", program[argument])
        return( program[argument] )
    else:
        if args.decode:
            print("\tImmediate mode;", argument, "is a value")
        return( argument ) 

def do_add(program, pos, modes):
    if args.verbose:
        print("\t", program[pos:pos+4])
    arg_a = decode_argument( program, program[pos+1], modes[0] )
    arg_b = decode_argument( program, program[pos+2], modes[1] )
    pos_t = program[pos+3]
    if args.verbose:
        print("\tSum values", arg_a, arg_b, "into", pos_t)
    program[pos_t] = arg_a + arg_b
    return( [0, 4] )

def do_mult(program, pos, modes):
    if args.verbose:
        print("\t", program[pos:pos+4])
    arg_a = decode_argument( program, program[pos+1], modes[0] )
    arg_b = decode_argument( program, program[pos+2], modes[1] )
    pos_t = program[pos+3]
    if args.verbose:
        print("\tMultiply values", arg_a, arg_b, "into", pos_t)
    program[pos_t] = arg_a * arg_b
    return( [0, 4] )

def do_input(program, pos):
    if args.verbose:
        print("\t", program[pos:pos+2])
    arg_a = program[pos+1]

    if len(args.input) == 0:
        print("Want to receive input but we have none!")
        exit(1)

    value = args.input.pop(0)
    if args.verbose:
        print("\tStoring input value", value, "at location", arg_a)
    program[arg_a] = value

    return( [0, 2] )

def do_output(program, pos, modes):
    if args.verbose:
        print("\t", program[pos:pos+2])
    arg_a = decode_argument( program, program[pos+1], modes[0] )

    print("Output:", arg_a)
    return( [0, 2] )

def do_jit(program, pos, modes):
    if args.verbose:
        print("\t", program[pos:pos+3])
    arg_a = decode_argument( program, program[pos+1], modes[0] )
    arg_b = decode_argument( program, program[pos+2], modes[1] )

    if arg_a != 0:
        if args.verbose:
            print("\t", arg_a, "is nonzero, jumping to", arg_b)
        return([1, arg_b])
    else:
        if args.verbose:
            print("\t", arg_a, "is zero, doing nothing")
        return([0, 3])

def do_jif(program, pos, modes):
    if args.verbose:
        print("\t", program[pos:pos+3])
    arg_a = decode_argument( program, program[pos+1], modes[0] )
    arg_b = decode_argument( program, program[pos+2], modes[1] )

    if arg_a == 0:
        if args.verbose:
            print("\t", arg_a, "is zero, jumping to", arg_b)
        return([1, arg_b])
    else:
        if args.verbose:
            print("\t", arg_a, "is nonzero, doing nothing")
        return([0, 3])

def do_lt(program, pos, modes):
    if args.verbose:
        print("\t", program[pos:pos+3])
    arg_a = decode_argument( program, program[pos+1], modes[0] )
    arg_b = decode_argument( program, program[pos+2], modes[1] )
    arg_c = program[pos+3]

    if arg_a < arg_b:
        if args.verbose:
            print("\t", arg_a, "is less than", arg_b, "; storing 1 at", arg_c)
        program[arg_c] = 1
    else:
        if args.verbose:
            print("\t", arg_a, "is not less than", arg_b, "; storing 0 at", arg_c)
        program[arg_c] = 0

    return([0, 4])

def do_eq(program, pos, modes):
    if args.verbose:
        print("\t", program[pos:pos+3])
    arg_a = decode_argument( program, program[pos+1], modes[0] )
    arg_b = decode_argument( program, program[pos+2], modes[1] )
    arg_c = program[pos+3]

    if arg_a == arg_b:
        if args.verbose:
            print("\t", arg_a, "is equal to", arg_b, "; storing 1 at", arg_c)
        program[arg_c] = 1
    else:
        if args.verbose:
            print("\t", arg_a, "is not equal to", arg_b, "; storing 0 at", arg_c)
        program[arg_c] = 0

    return([0, 4])

def compute(program):
    pos=0
    while(1):
        if args.verbose:
            print("# Looking for opcode at", pos, ":", program[pos])

        opcode = program[pos] % 100
        modes = [ ( program[pos] // dec ) % 10 for dec in [ 100, 1000, 10000 ] ]

        if opcode == 99:
            return
        elif opcode == 1:
            inst_len = do_add(program, pos, modes)
        elif opcode == 2:
            inst_len = do_mult(program, pos, modes)
        elif opcode == 3:
            inst_len = do_input(program, pos)
        elif opcode == 4:
            inst_len = do_output(program, pos, modes)
        elif opcode == 5:
            inst_len = do_jit(program, pos, modes)
        elif opcode == 6:
            inst_len = do_jif(program, pos, modes)
        elif opcode == 7:
            inst_len = do_lt(program, pos, modes)
        elif opcode == 8:
            inst_len = do_eq(program, pos, modes)
        else:
            print("Unrecognised opcode", opcode, "at position", pos)
            print(program)
            exit(1)

        if inst_len[0] == 0:    # We've returned a relative jump for pos
            pos += inst_len[1]
        elif inst_len[0] == 1:  # Absolute position
            pos = inst_len[1]
        else:
            print("Unexpected return type", inst_len[0])
            exit(1)

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

    compute(program)
