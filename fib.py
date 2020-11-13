import sys

def fib(n):
    # Fibonacci equation is n = n-1 + n-2
    # base case
    if n == 0:
        return 0
    # other base case
    elif n == 1:
        return 1
    # recurse
    else:
        print(n)
        return fib(n-1) + fib(n-2)

input = int(sys.argv[1])
n = fib(input)
print(n)