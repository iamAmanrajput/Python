# HTML HEADER TEXT SPLITTER TECHNIQUE

from langchain_text_splitters import HTMLHeaderTextSplitter

# Sample HTML content
html_string = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>
<body>
    <h1>Foo</h1>
    <p>Some intro about foo.</p>
    <div>
        <h2>Bar main section</h2>
        <p>Some intro text about Bar.</p>
        <h3>Bar subsection 1</h3>
        <p>Some text about the first subtopic of Bar.</p>
        <h3>Bar subsection 2</h3>
        <p>Some text about the second subtopic of Bar.</p>
    </div>
    <div>
        <div>
            <h2>Baz</h2>
            <p>Some text about Baz</p>
        </div>
        <br>
        <p>Some concluding text about Foo</p>
    </div>
</body>
</html>
"""

# HTML ko kin header tags ke basis par split karna hai
headers_to_split_on = [
    ("h1", "Header 1"),
    ("h2", "Header 2"),
    ("h3", "Header 3"),
]

# HTML Header Text Splitter create karo
# Ye HTML document ko h1, h2 aur h3 tags ke basis par split karega
html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

# HTML content ko headers ke basis par chunks me divide karo
# Har chunk ke saath uske corresponding header metadata bhi preserve rahega
html_header_splits = html_splitter.split_text(html_string)

print(html_header_splits)

# [Document(metadata={'Header 1': 'Foo'}, page_content='Foo'), Document(metadata={'Header 1': 'Foo'}, page_content='Some intro about foo.'), Document(metadata={'Header 1': 'Foo', 'Header 2': 'Bar main section'}, page_content='Bar main section'),Document(metadata={'Header 1': 'Foo', 'Header 2': 'Bar main section'}, page_content='Some intro text about Bar.'), Document(metadata={'Header 1': 'Foo', 'Header 2': 'Bar main section', 'Header 3': 'Bar subsection 1'}, page_content='Bar subsection 1'), Document(metadata={'Header 1': 'Foo', 'Header 2': 'Bar main section', 'Header 3': 'Bar subsection 1'}, page_content='Some text about the first subtopic of Bar.'), Document(metadata={'Header 1': 'Foo', 'Header 2': 'Bar main section', 'Header 3': 'Bar subsection 2'}, page_content='Bar subsection 2'), Document(metadata={'Header 1': 'Foo', 'Header 2': 'Bar main section', 'Header 3': 'Bar subsection 2'}, page_content='Some text about the second subtopic of Bar.'), Document(metadata={'Header 1': 'Foo', 'Header 2': 'Baz'}, page_content='Baz'), Document(metadata={'Header 1': 'Foo'}, page_content='Some text about Baz  \nSome concluding text about Foo')]