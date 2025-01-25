from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    book_id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, book_id, title, author, description, rating, published_date):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    book_id: Optional[int] = Field(default=None, description="ID is not needed on creation")
    title: str = Field(min_length=3, max_length=30)
    author: str = Field(min_length=3, max_length=30)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(ge=2000, le=2026)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Book title",
                "author": "<NAME>",
                "description": "Book description",
                "rating": 2,
                "published_date": 2010
            }
        }
    }

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2010),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2005),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2005),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2010),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2020),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2020)
    ]

#GET
@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.book_id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_books_by_rating(book_rating: int=Query(gt=0, lt=6)):
    books_to_return=[]
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

@app.get("/books/pub_date/", status_code=status.HTTP_200_OK)
async def read_books_by_published_date(published_date: int=Query(gt=2000, lt=2026)):
    books_to_return=[]
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


#POST
@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.book_id = 1 if len(BOOKS) == 0 else BOOKS[-1].book_id + 1
    return book

#PUT Request
@app.put("/books/update-book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].book_id == book.book_id:
            BOOKS[i] = Book(**book.model_dump())
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")


#DELETE Request
@app.delete("/books/{book_id_to_delete}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id_to_delete: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].book_id == book_id_to_delete:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")
