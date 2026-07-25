# Import required libraries
from langchain_ollama import OllamaLLM
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# Create a chat prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond to the question asked"),
    ("user", "Question: {question}")
])


# Create the Streamlit user interface
st.title("LangChain Demo With Ollama")
input_text = st.text_input("What question do you have in mind?")


# Initialize the Ollama LLM
llm = OllamaLLM(model="gemma3:latest")


# Create an output parser to convert the model response into a string
output_parser = StrOutputParser()


# Create the LangChain pipeline using LCEL
chain = prompt | llm | output_parser


# Invoke the chain when the user enters a question
if input_text:
    st.write(chain.invoke({"question": input_text}))