# Problem Statement:
# Write a Python program that suggests an activity based on the weather.
# - If the weather is "Sunny", the activity should be "Go for a walk".
# - If the weather is "Rainy", the activity should be "Read a book".
# - If the weather is "Snowy", the activity should be "Build a snowman".
# Finally, print the suggested activity.

weather = "Sunny"

if weather == "Sunny":
    activity = "Go for a walk"
elif weather == "Rainy":
    activity = "Read a book"
elif weather == "Snowy":
    activity = "Build a snowman"

print(activity)
