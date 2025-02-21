count = 0
for number in range(1, 10):
    if number % 2 == 0:  # if the number is even, the % is a modulo operator, dividing the number by 2 and checking if the remainder is 0 means it is even
        count += 1
        print(number)
# this is a formatted string so we can use the variable count in the string to indicate how many times we printed an even number
print(f"We have {count} even numbers")
