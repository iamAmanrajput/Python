# Problem Statement:
# Write a Python program to assign a grade based on a student's score.
# - If the score is greater than 100, print "Please verify your grade again" and stop the program.
# - If the score is between 90 and 100, assign grade "A".
# - If the score is between 80 and 89, assign grade "B".
# - If the score is between 70 and 79, assign grade "C".
# - If the score is between 60 and 69, assign grade "D".
# - If the score is below 60, assign grade "F".
# Finally, print the grade.

score = 185

if score >= 101:
    print("Please verify your grade again")
    exit()

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print("Grade: ", grade)
