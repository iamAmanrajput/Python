# importing random library
import random

# 1. Generate a random float number between 0 and 1
num1 = random.random()
print("Random float between 0 and 1:", num1)

# 2. Generate a random integer between 1 and 10 (inclusive)
num2 = random.randint(1, 10)
print("Random integer between 1 and 10:", num2)

# 3. Generate a random number from a range with step
num3 = random.randrange(1, 20, 2)  # odd numbers only between 1 and 20
print("Random odd number between 1 and 20:", num3)

# 4. Pick a random element from a list
fruits = ["apple", "banana", "mango", "grapes", "orange"]
choice = random.choice(fruits)
print("Randomly chosen fruit:", choice)

# 5. Shuffle a list (changes the order randomly)
numbers = [1, 2, 3, 4, 5]
random.shuffle(numbers)
print("Shuffled list:", numbers)

# 6. Generate a random float number between given range
num4 = random.uniform(10, 20)  # between 10 and 20
print("Random float between 10 and 20:", num4)

# 7. Select multiple random elements from a list
sample_items = random.sample(fruits, 3)  # pick 3 unique random fruits
print("3 Random fruits:", sample_items)

# Random float between 0 and 1: 0.5623135699732831
# Random integer between 1 and 10: 7
# Random odd number between 1 and 20: 13
# Randomly chosen fruit: mango
# Shuffled list: [4, 2, 5, 3, 1]
# Random float between 10 and 20: 14.7832976138219
# 3 Random fruits: ['apple', 'mango', 'orange']
