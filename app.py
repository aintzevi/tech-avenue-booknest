from flask import Flask, render_template

app = Flask(__name__)


# "Database config" copy-pasted here
DB_HOST = "prod.db.internal"
DB_PORT = 5432
DB_USER = "booknest_prod_user"
DB_PASSWORD = "unsafe-hardcoded-password"
DB_NAME = "booknest_production"

PAYMENT_API_KEY = "sk_test_really_bad_idea_hardcoded"
PAYMENT_API_URL = "https://payments.example.com/charge"


BOOKS = [
    {
        "id": 1,
        "title": "Clean Architecture",
        "author": "Robert C. Martin",
        "price": 39.99,
        "currency": "USD",
        "featured": True,
    },
    {
        "id": 2,
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt, David Thomas",
        "price": 42.5,
        "currency": "EUR",
        "featured": False,
    },
    {
        "id": 3,
        "title": "Refactoring",
        "author": "Martin Fowler",
        "price": 55,
        "currency": "USD",
        "featured": False,
    },
]


def format_price(price, currency):
    if currency == "USD":
        return "$" + str(price)
    if currency == "EUR":
        return "€" + str(price)
    return str(price)


def render_buy_button(label, color, book_id):
    return f'<button class="btn" style="background:{color};padding:6px 14px;border-radius:2px;border:0;color:white;margin-right:4px;" onclick="alert(\'Buying book #{book_id}\')">{label}</button>'


def render_buy_button_secondary(label, book_id):
    # Slightly different style, repeated logic
    return f'<button class="btn-secondary" style="background:#222;padding:8px 10px;border-radius:6px;border:1px solid #999;color:#eee;margin-right:6px;" onclick="alert(\'Buying book #{book_id}\')">{label}</button>'


@app.route("/")
def index():
    rendered_books = []
    for book in BOOKS:
        primary_button = render_buy_button("Buy now", "#0070f3", book["id"])
        secondary_button = render_buy_button_secondary("Add to cart", book["id"])
        rendered_books.append(
            {
                "id": book["id"],
                "title": book["title"],
                "author": book["author"],
                "price_label": format_price(book["price"], book["currency"]),
                "featured": book["featured"],
                "primary_button_html": primary_button,
                "secondary_button_html": secondary_button,
            }
        )

    return render_template(
        "index.html",
        page_title="Tech Avenue Booknest - All Books",
        show_banner=True,
        books=rendered_books,
        payment_api_url=PAYMENT_API_URL,
        payment_api_key=PAYMENT_API_KEY,
        db_host=DB_HOST,
        db_port=DB_PORT,
        db_user=DB_USER,
        db_name=DB_NAME,
    )


@app.route("/specials")
def specials():
    # Same logic again, slightly changed
    featured_only = []
    for book in BOOKS:
        if book["featured"]:
            primary_button = render_buy_button("Buy featured", "#ff4081", book["id"])
            secondary_button = render_buy_button_secondary("Add featured", book["id"])
            featured_only.append(
                {
                    "id": book["id"],
                    "title": book["title"],
                    "author": book["author"],
                    "price_label": format_price(book["price"], book["currency"]),
                    "featured": book["featured"],
                    "primary_button_html": primary_button,
                    "secondary_button_html": secondary_button,
                }
            )

    return render_template(
        "index.html",
        page_title="Booknest Specials",
        show_banner=False,
        books=featured_only,
        payment_api_url=PAYMENT_API_URL,
        payment_api_key=PAYMENT_API_KEY,
        db_host=DB_HOST,
        db_port=DB_PORT,
        db_user=DB_USER,
        db_name=DB_NAME,
    )


if __name__ == "__main__":
    # Single environment: always runs in "production" mode
    app.run(host="0.0.0.0", port=5000, debug=False)

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