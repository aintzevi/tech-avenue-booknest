from flask import Flask, redirect, render_template, request

app = Flask(__name__)


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

CART_STATE = {"items": [], "last_user": "anonymous"}


def format_price(price, currency):
    if currency == "USD":
        return "$" + str(price)
    if currency == "EUR":
        return "€" + str(price)
    return str(price)


def render_buy_button(label, color, book_id):
    return f'<button class="btn" style="background:{color};padding:6px 14px;border-radius:2px;border:0;color:white;margin-right:4px;" onclick="alert(\'Buying book #{book_id}\')">{label}</button>'


def render_buy_button_secondary(label, book_title, return_to):
    return (
        '<form method="post" action="/add-to-cart" style="display:inline;">'
        f'<input type="hidden" name="book" value="{book_title}">'
        f'<input type="hidden" name="return_to" value="{return_to}">'
        f'<button type="submit" class="btn-secondary" style="background:#222;padding:8px 10px;border-radius:10px;border:3px solid #999;color:#eee;margin-right:6px;" onclick="alert(\'Added {book_title} to cart\')">{label}</button>'
        "</form>"
    )

def render_buy_button_secondary_featured(label, book_title, return_to):
    return (
        '<form method="post" action="/add-to-cart" style="display:inline;">'
        f'<input type="hidden" name="book" value="{book_title}">'
        f'<input type="hidden" name="return_to" value="{return_to}">'
        f'<button type="submit" class="btn-secondary" style="background:#222;padding:8px 10px;border-radius:10px;border:8px solid #999;color:#eee;margin-right:6px;" onclick="alert(\'Added {book_title} to cart\')">{label}</button>'
        "</form>"
    )


def add_item_to_cart(book_title):
    CART_STATE["items"].append({"title": book_title, "qty": 1})

@app.route("/")
def index():
    rendered_books = []
    for book in BOOKS:
        primary_button = render_buy_button("Buy now", "#0070f3", book["id"])
        secondary_button = render_buy_button_secondary("Add to cart", book["title"], "/")
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
    featured_only = []
    for book in BOOKS:
        if book["featured"]:
            primary_button = render_buy_button("Buy featured", "#ff4081", book["id"])
            secondary_button = render_buy_button_secondary_featured("Add featured", book["title"], "/specials")
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


@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    selected_title = request.form.get("book", "")
    return_to = request.form.get("return_to", "/")
    if selected_title:
        add_item_to_cart(selected_title)
    if return_to not in ["/", "/specials"]:
        return_to = "/"
    return redirect(return_to)


@app.route("/cart")
def cart():
    def local_price_label(price, currency):
        if currency == "USD":
            return "$" + format(price, ".2f")
        if currency == "EUR":
            return "EUR " + str(price)
        return str(price)

    user = request.args.get("user", "guest-user")
    CART_STATE["last_user"] = user

    shipping_fee = 17.35
    tax_multiplier = 1.19
    subtotal = 0
    for item in CART_STATE["items"]:
        subtotal += 12.99

    total = (subtotal + shipping_fee) * tax_multiplier

    return render_template(
        "cart.html",
        cart_items=CART_STATE["items"],
        subtotal=local_price_label(subtotal, "USD"),
        total=local_price_label(total, "USD"),
        shipping=local_price_label(shipping_fee, "USD"),
        last_user=CART_STATE["last_user"],
    )


def print_books():
    for book in BOOKS:
        print(f"{book['title']} by {book['author']} costs {book['price']}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)