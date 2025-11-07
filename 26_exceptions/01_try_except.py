try:
    # risky code
    number = int(input("Enter a number: "))
    result = 10 / number
    print("Result:", result)

except ValueError:
    # runs if input is not a valid number
    print("Error: Please enter a valid integer.")

except ZeroDivisionError:
    # runs if user enters 0
    print("Error: Number cannot be zero.")

finally:
    # always runs (error aaye ya na aaye)
    print("Thank you for using the program!")


# -------------------------------
# CASE 1 (Valid input → e.g., 5)
# Input:
# Enter a number: 5
# Output:
# Result: 2.0
# Thank you for using the program!
# -------------------------------

# CASE 2 (ZeroDivisionError)
# Input:
# Enter a number: 0
# Output:
# Error: Number cannot be zero.
# Thank you for using the program!
# -------------------------------

# CASE 3 (ValueError)
# Input:
# Enter a number: abc
# Output:
# Error: Please enter a valid integer.
# Thank you for using the program!
# -------------------------------