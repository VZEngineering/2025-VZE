while True:
    command = input(">")
    print("ECHO", command)  # this will print the command that the user inputs
    if command.lower() == "quit":  # this will put the command in lower case and compare it with "quit" so any case can work
        break  # this will break the loop if the user inputs "quit"

# need to make sure to always have a break when using a while loop to avoid infinite loops
