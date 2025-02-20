for number in range(3):
    # this multiplies the dot by the number of attempts
    print("Attempt", number+1, (number + 1) * ".")

print("")

for number in range(1, 4):
    # this will output the same as above but more concise
    print("Attempt", number, number * ".")

print("")

for number in range(1, 10, 2):  # start, stop, step (increment)
    print("Attempt", number, number * ".")

print("")
