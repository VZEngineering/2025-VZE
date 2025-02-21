""" This is a python exercise created by Grok 3 for me to solve - 
Finished and updated with assistance from AI """


def temperature_data():
    """ This function takes daily temp input from the user"""
    daily_temperatures = []  # empty list to store the temperatures
    for i in range(7):  # 7 days in a week
        while True:
            try:        # try to convert the input to a float
                temp = float(
                    input(f"Enter the temperature for day {i + 1} in Celsius: "))
                # add the temperature to the end of the list
                daily_temperatures.append(temp)
                break
            except ValueError:  # if the user enters a non-numeric value
                print("Please enter a valid temperature!")
    return daily_temperatures  # return the list of temperatures


# Store the temperatures in a variable so that we can use it later without calling
# the function again
temperatures = temperature_data()

# calculate the average temperature for the week
week_average_temp = sum(temperatures) / 7
hot_days = [temp for temp in temperatures if temp >
            30]  # list of hot days

# average temperature
print(
    # average temperature \u00B0 is the unicode for the degree symbol and putting C shows celsius
    f"\nAverage temperature for the week: {week_average_temp:.2f}\u00B0C")
print(f"Number of hot days: {len(hot_days)}")  # number of hot days
