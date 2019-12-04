#!/usr/bin/python3

import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("min", help="Minimum range", type=int)
parser.add_argument("max", help="Maximum range", type=int)
parser.add_argument("--part2", help="More complex check for double digits", action="store_true")
args = parser.parse_args()

total_valid = 0
for i in range ( args.min, args.max + 1 ):
    valid = True
    str_i=str(i)

    # It is a six digit number
    if len(str_i) != 6:
        valid = False
        continue

    # Two adjacent digits are the same
    # Digits never decrease

    double = False
    lastdigit = str_i[0]
    for d in str_i[1:]:
        if lastdigit == d:
            double = True
        if int(d) < int(lastdigit):
            valid = False
            break
        lastdigit = d

    if not args.part2 and not double:
        valid = False

    # Part 2: ONLY two adjacent digits are the same

    if args.part2:
        exactly_double = False
        for j in range(0, len(str_i)):
            if j > 0 and str_i[j] == str_i[j-1]:
                continue

            count = 1
            k = j + 1
            while k < len(str_i) and str_i[k] == str_i[j]:
                count += 1
                k += 1

            if count == 2:
                exactly_double = True

        if not exactly_double:
            valid = False

    if valid:
        total_valid += 1

print(total_valid, "valid passwords")
