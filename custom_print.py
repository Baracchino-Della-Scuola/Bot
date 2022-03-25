import sys

print = lambda x, end="\n" : sys.stdout.write(x+end)

print("hi", end="Nope")
print("oof")