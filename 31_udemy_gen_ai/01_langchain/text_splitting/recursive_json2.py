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

documents = splitter.create_documents(texts=[json_data])

print(documents)

# [Document(metadata={}, page_content='{"company": {"name": "OpenAI", "location": "San Francisco"}}'), Document(metadata={}, page_content='{"company": {"employees": [{"name": "Aman", "role": "Developer", "skills": ["Python", "LangChain", "AI"]},{"name": "Rahul", "role": "Designer", "skills": ["Figma", "UI/UX"]}]}}')]