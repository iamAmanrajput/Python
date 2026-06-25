from langchain_text_splitters import RecursiveJsonSplitter

# Sample JSON data
json_data = {
    "company": {
        "name": "OpenAI",
        "location": "San Francisco",
        "employees": [
            {
                "name": "Aman",
                "role": "Developer",
                "skills": ["Python", "LangChain", "AI"]
            },
            {
                "name": "Rahul",
                "role": "Designer",
                "skills": ["Figma", "UI/UX"]
            }
        ]
    }
}

# Create Recursive JSON Splitter
splitter = RecursiveJsonSplitter(max_chunk_size=100)

# Split JSON into chunks
chunks = splitter.split_json(json_data)

# Print chunks
for i, chunk in enumerate(chunks, start=1):
    print(f"Chunk {i}:")
    print(chunk)
    print("-" * 50)


# Chunk 1:
# {'company': {'name': 'OpenAI', 'location': 'San Francisco'}}
# --------------------------------------------------
# Chunk 2:
# {'company': {'employees': [{'name': 'Aman', 'role': 'Developer', 'skills': ['Python', 'LangChain', 'AI']}, {'name': 'Rahul', 'role': 'Designer', 'skills': ['Figma', 'UI/UX']}]}}
# --------------------------------------------------