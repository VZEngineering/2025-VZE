print(type(5))
print(type(range(5)))  # <class 'range'> is a complex iterable type

# iterable means that you can iterate over it and use it in a for loop

for x in "python":  # string is an iterable as well
    print(x)

# python also has a while loop

number = 100
while number > 0:
    print(number)
    number //= 2

command = ""
while command.lower != "quit":  # this will put the command in lower case and compare it with "quit" so any case can work
    command = input(">")
    print("ECHO", command)
