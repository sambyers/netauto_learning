import math

TOLERANCE = 0.000001
def newton(x, estimate):
    estimate = (estimate + x / estimate) / 2
    difference = abs(x - estimate ** 2)
    if difference <= TOLERANCE:
        return estimate
    else:
        print(x, estimate)
        return newton(x, estimate)

x = input("Enter a positive number... ")
x = float(x)
print("The program estimate is ", newton(x, 1.0))
print("Python's estimate is ", math.sqrt(x))