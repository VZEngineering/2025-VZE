# This below takes an input to ask if you are successful and puts it in lower case and compares if equal to yes
# to get a boolean value and runds the for loop depending on your answer.
succsessful = input("Are you successful? Yes or No: ").lower() == "yes"
for number in range(3):
    print("Thinking")
    if succsessful:
        print("Spectacular")
        break  # this will break the loop after being successful
else:
    # this will only run if the loop is not broken
    print("Loser")
