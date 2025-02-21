""" This is a function module to learn how to make a function """


def greet():  # this names the function, it should be descriptive
    print("Hello there")
    print("Welcome aboard")


greet()  # this calls the function and does not take an input


def greet_user(first_name, last_name):
    print(f'Hi {first_name} {last_name}!')
    print('Welcome aboard')


# this calls the function and takes two inputs
greet_user("Camron", "Vogelzang")
greet_user("John", "Smith")
