def multiply(*numbers):
    total = 1
    for number in numbers:
        # total = total * number (this line has the same effect as the line below but this one is not condensed)
        total *= number
    return (total)


print(multiply(2, 3, 4, 5))
