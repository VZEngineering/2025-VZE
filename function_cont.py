def greet(name):
    print(f"Hi {name}!")


def get_greeting(name):
    # return the greeting message to the caller and it does not print only if called
    return f"Hi {name}!"


message = get_greeting("Camron")

print(message)  # Hi Camron!
