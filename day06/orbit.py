#!/usr/bin/python3

import argparse

orbitcache = {}
def count_orbits(body, target='COM'):
    if body == target:
        return(0)
    if body not in orbitcache:
        parent = orbits[body]
        count = count_orbits(parent, target) + 1
        if args.verbose:
            print("Body", body, "is", count, "transfers from", target)
        orbitcache[body] = count
    return(orbitcache[body])

def get_parents(body):
    if body not in orbits:
        return([])
    else:
        parent = orbits[body]
        return([parent] + get_parents(parent))

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="Print out each instruction as executed", action="store_true")
parser.add_argument("--part2", help="Calculate orbital transfers from YOU to SAN", action="store_true")
parser.add_argument("filename", help="orbit source")
args = parser.parse_args()

inputfile = open(args.filename)
orbits = {}
for line in inputfile:
    [ parent, child ] = line[:-1].split(')')
    orbits[child] = parent

if not args.part2:
    total = 0
    for body in orbits.keys():
        total += count_orbits(body)

    print("Total orbits:", total)
    exit(0)

for ver in [ 'SAN', 'YOU' ]:
    if ver not in orbits: 
        print(ver, "not present in orbits!")
        exit(1)

san_parents = get_parents('SAN')
my_parents  = get_parents('YOU')

print( san_parents )
print( my_parents )

for common in san_parents:
    if common in my_parents:
        if args.verbose:
            print("Found", common, "as lowest orbital denominator")
        break
else:
    print("No common orbital denominator")
    exit(1)

transfers_out = count_orbits(orbits['YOU'], common)
transfers_in = count_orbits(orbits['SAN'], common)

print("Total transfers from YOU to SAN via", common, transfers_out + transfers_in)
