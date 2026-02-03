import tiktoken  # Library used to convert text into tokens and back

# Load tokenizer (encoding) that works with the GPT-4o model
enc = tiktoken.encoding_for_model("gpt-4o")

# Text that we want to convert into tokens
text = "Hey There! My name is Aman Singh"

# Convert the text into tokens (numbers)
# Each token is a number that represents part of the text
tokens = enc.encode(text)

# Print the list of tokens
print("Tokens:", tokens)
# Example:
# Tokens: [25216, 3274, 0, 3673, 1308, 382, 117747, 44807]

# Convert tokens back into readable text
decoded_text = enc.decode(tokens)

# Print the decoded text
print("Decoded Text:", decoded_text)
# Output:
# Hey There! My name is Aman Singh
