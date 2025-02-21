def increment(number, by=1):
    return number + by


# result = increment(2, 1)
# print(result)
# (the code here is the same as below)
# the code below is more readable

# by=1 is a keyword argument and makes your code more readable
# by not calling a second argument, it will use the default value of 1
print(increment(2))
# by calling a second argument, it will use the value of 5 and overwite the default value of 1
print(increment(2, 5))
