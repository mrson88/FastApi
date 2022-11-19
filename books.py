from typing import Optional

from fastapi import FastAPI
from enum import Enum

app = FastAPI()

BOOKS = {
    'book_1': {'title': 'Title One', 'author': 'Author One'},
    'book_2': {'title': 'Title Two', 'author': 'Author Two'},
    'book_3': {'title': 'Title Three', 'author': 'Author Three'},
    'book_4': {'title': 'Title Four', 'author': 'Author Four'},
    'book_5': {'title': 'Title Five', 'author': 'Author Five'},
}


class DirectioName(str, Enum):
    north = 'North'
    south = 'South'
    east = 'East'
    west = 'West'


@app.get('/')
async def read_all_books(skip_book: Optional[str] = None):
    if skip_book:
        new_book = BOOKS.copy()
        del new_book[skip_book]
        return new_book
    return BOOKS


@app.get('/direction/{direction_name}')
async def get_direction(direction_name: DirectioName):
    if direction_name == DirectioName.north:
        return {'Direction': direction_name, 'sub': 'Up'}
    if direction_name == DirectioName.south:
        return {'Direction': direction_name, 'sub': 'Down'}
    if direction_name == DirectioName.west:
        return {'Direction': direction_name, 'sub': 'Left'}
    if direction_name == DirectioName.east:
        return {'Direction': direction_name, 'sub': 'Right'}


@app.get('/{book_name}')
async def read_book(book_name: str):
    return BOOKS[book_name]


@app.post('/')
async def creat_book(book_title, book_author):
    current_book_id = 0
    if len(BOOKS) > 0:
        for book in BOOKS:
            x = int(book.split('_')[-1])
            current_book_id = x
    BOOKS[f'book_{current_book_id + 1}'] = {'title': book_title, 'author': book_author}
    return BOOKS[f'book_{current_book_id + 1}']


@app.put('/{book_name}')
async def update_book(book_name: str, book_title: str, book_author: str):
    book_infomation = {'title': book_title, 'author': book_author}
    BOOKS[book_name] = book_infomation
    return book_infomation


@app.delete('/{book_name}')
async def delete_book(book_name):
    del BOOKS[book_name]
    return f'{book_name} delete.'


'1. Create a new read book function that uses query params instead of path params.'

'2. Create a new delete book function that uses query params instead of path params.'


@app.get('/assignment/')
async def read_book_assignment(book_name: str = None):
    if book_name:
        return BOOKS[book_name]
    return BOOKS


@app.delete('/assignment/')
async def delete_book_assignment(book_name: str):
    del BOOKS[book_name]
    return BOOKS
