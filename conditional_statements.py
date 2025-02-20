temperature = 65  # Change the value to test the code
if temperature > 70:  # If the temperature is greater than 70
    print("It's hot outside!")  # Print this message
elif temperature > 50:  # If the temperature is greater than 20
    print("It's warm outside!")  # Print this message
else:  # If the temperature is not greater than 70
    print("It's cold outside!")  # Print this message
print("Done!")  # Print this message regardless of the temperature


# A simpler way to do if statements is as follows

# age = 22
# if age >= 18:
#    message = "You are old enough to vote!"
# else:
#    message = "You are not old enough to vote."
# This code below works exactly like the code above but is more concise, this is called a turnary operator
# The turnary operator is a way to write an if statement in one line utilizing a variable
age = 22
message = "You are old enough to vote!" if age >= 18 else "You are not old enough to vote."
print(message)
