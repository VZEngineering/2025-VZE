"""_This is my python learning file"""

first = "Camron"
last = "Vogelzang"
# full = first + " " + last # Concatenation to build a string, old approach
full = f"{first} {last}"  # f-string (formatted string), new approach
print(full)  # Camron Vogelzang


course = "      Python Programming"
print(course.upper())  # This will print the course in upper case
print(course.lower())  # This will print the course in lower case
print(course.title())  # This will print the course in its original form
print(course)  # This will print the course in its original form

# This will print the index of the first occurrence of the string "Pro"
print(course.find("Pro"))

# This will replace all occurrences of the letter "P" with a hyphen
print(course.replace("P", "-"))

# This will check if the string "Pro" is in the course string
print("Pro" in course)

# This will print True
print("swift" not in course)
