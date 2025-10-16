# Match-Case (Switch) Example in Python

day = input("Enter day number (1-3): ")

match day:
    case "1":
        print("Monday")
    case "2":
        print("Tuesday")
    case "3":
        print("Wednesday")
    case _:
        print("Invalid day")


# Enter day number (1-3): 1
# Monday
