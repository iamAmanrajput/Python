# HTML HEADER TEXT SPLITTER TECHNIQUE

from langchain_text_splitters import HTMLHeaderTextSplitter

url = "https://plato.stanford.edu/entries/goedel/"

headers_to_split_on = [
    ("h1", "Header 1"),
    ("h2", "Header 2"),
    ("h3", "Header 3"),
    ("h4", "Header 4"),
]

html_splitter = HTMLHeaderTextSplitter(headers_to_split_on)

html_header_splits = html_splitter.split_text_from_url(url)

print(html_header_splits)