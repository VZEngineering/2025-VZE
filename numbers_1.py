"""In Python you have three types of numbers: integers, floating-point numbers, and complex numbers."""

import math  # import the math module

x = 1  # int
y = 2.8  # float
z = 1j  # complex number, j is the imaginary part of the complex number

# there are are four types of mathematical operations in Python: addition, subtraction, multiplication, and division

print(x + y)  # 3.8 # addition
print(x - y)  # -1.8 # subtraction
print(x * y)  # 2.8 # multiplication
print(x / y)  # 0.35714285714285715 # division, the result is a float
# 0.0 # floor division, the result is rounded down to the nearest whole number
print(x // y)
print(x % y)  # 1.0 # remainder of the division of x by y
print(x ** y)  # 1.0 # x to the power of y (x^y)

round(3.75)  # 4 # round a number to the nearest whole number
abs(-3.75)  # 3.75 # return the absolute value of a number
print(abs(-3.75))  # prints the absolute value of the number

print(math.ceil(2.2))  # 3 # round a number up to the nearest whole number

print(10 % 3)  # % is the modulus operator, it returns the remainder of the division of the number to the left by the number on its right
