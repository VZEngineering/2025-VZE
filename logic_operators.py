high_income = False
good_credit = True
student = False

if high_income and good_credit:
    # This will print because both conditions are true, no need to add True in the statement
    print("Eligible for loan")
else:
    # This will not print because both conditions are true
    print("Not eligible for loan")

if high_income or good_credit:  # This will print because one of the conditions is true
    print("Eligible for loan")
else:
    print("Not eligible for loan")

if high_income and not good_credit:  # This will not print because one of the conditions is false
    print("Eligible for loan")
else:
    print("Not eligible for loan")

if (high_income or good_credit) and not student:  # This will print because all conditions are true
    print("Eligible for loan")
else:
    print("Not eligible for loan")
