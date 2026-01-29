from typing import List, Optional
from pydantic import BaseModel


# -------------------------------
# Comment Model (Self-Referencing Model)
# -------------------------------
# Ye model ek comment ko represent karta hai
# replies field khud isi Comment model ki list ho sakti hai
class Comment(BaseModel):
    id: int                 # Comment ka unique ID
    content: str            # Comment ka text/content
    replies: Optional[List["Comment"]] = None
    # replies:
    # - Optional hai (comment ke replies ho bhi sakte hain ya nahi bhi)
    # - List["Comment"] matlab replies bhi same structure ke honge (self reference)


# -------------------------------
# Forward Reference Resolve
# -------------------------------
# Kyunki humne "Comment" ko string me use kiya hai,
# isliye model_rebuild() call karke Pydantic ko batate hain
# ki ab model complete ho chuka hai
Comment.model_rebuild()


# -------------------------------
# Comment Object Create karna
# -------------------------------
# Ek parent comment banaya jisme multiple replies hain
# Aur un replies ke andar bhi nested reply hai
comment = Comment(
    id=1,
    content="First comment",
    replies=[
        Comment(id=2, content="reply 1"),
        Comment(
            id=3,
            content="reply 2",
            replies=[
                Comment(id=4, content="nested reply")
            ]
        )
    ]
)

# Final validated object print
print(comment)


# id=1 content='First comment' replies=[
#     Comment(id=2, content='reply 1', replies=None),
#     Comment(id=3, content='reply 2', replies=[
#         Comment(id=4, content='nested reply', replies=None)
#     ])
# ]
