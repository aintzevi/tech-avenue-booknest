# Hardcoded book data
books = [
    {'title': 'Book One', 'author': 'Author One', 'price': 9.99},
    {'title': 'Book Two', 'author': 'Author Two', 'price': 14.99},
]


# Function to print books
 def print_books():
    for book in books:
        print(f"Title: {book.get('title')}, Author: {book.get('author')}, Price: {book.get('price')}")


# Starting point
if __name__ == '__main__':
    print_books()