import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    portfolio = db.execute(
        "SELECT symbol, shares FROM portfolio WHERE user_id = ?", session["user_id"])

    portfolio_list = []
    portfolio_total_value = 0
    for stock in portfolio:
        quote = lookup(stock["symbol"])
        if quote:
            total_value = stock["shares"] * quote["price"]
            portfolio_list.append({
                "symbol": stock["symbol"],
                "shares": stock["shares"],
                "price": quote["price"],
                "total_value": total_value
            })
            portfolio_total_value += total_value

    user_cash = float(db.execute("SELECT cash FROM users WHERE id = ?",
                      session["user_id"])[0]["cash"])

    user_total_cash = user_cash + portfolio_total_value

    return render_template("index.html", current_prices=portfolio_list, user_cash=user_cash, user_total_cash=user_total_cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        symbol_data = lookup(request.form.get("symbol"))
        shares = request.form.get("shares")

        if not symbol_data:
            return apology("INVALID SYMBOL")

        if not shares.isdigit() or int(shares) < 1:
            return apology("INVALID SHARES")

        total_price = float(symbol_data["price"]) * int(shares)

        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

        if total_price > float(user_cash[0]["cash"]):
            return apology("CAN'T AFFORD")
        else:
            try:
                db.execute("BEGIN")

                db.execute(
                    "INSERT INTO transactions (user_id, type, symbol, shares, price) VALUES (?, ?, ?, ?, ?)",
                    session["user_id"],
                    "BUY",
                    symbol_data["symbol"],
                    int(shares),
                    float(symbol_data["price"])
                )

                existing = db.execute(
                    "SELECT shares FROM portfolio WHERE user_id = ? AND symbol = ?",
                    session["user_id"],
                    symbol_data["symbol"]
                )
                if existing:
                    db.execute(
                        "UPDATE portfolio SET shares = shares + ? WHERE user_id = ? AND symbol = ?",
                        int(shares),
                        session["user_id"],
                        symbol_data["symbol"]
                    )
                else:
                    db.execute(
                        "INSERT INTO portfolio (user_id, symbol, shares) VALUES (?, ?, ?)",
                        session["user_id"],
                        symbol_data["symbol"],
                        int(shares)
                    )

                db.execute(
                    "UPDATE users SET cash = cash - ? WHERE id = ?",
                    total_price,
                    session["user_id"]
                )

                # Підтверджуємо транзакцію
                db.execute("COMMIT")
                return redirect("/")

            except Exception as e:
                db.execute("ROLLBACK")
                return apology("Something went wrong", 500)

    if request.method == "GET":
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    transactions = db.execute(
        "SELECT symbol, shares, price, timestamp FROM transactions WHERE user_id = ?", session["user_id"])

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        symbol_data = lookup(symbol)

        if symbol_data:
            return render_template("quoted.html", symbol_data=symbol_data)

        else:
            return apology("INVALID SYMBOL")

    if request.method == "GET":
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Must provide username", 400)

        if not password:
            return apology("Must provide password", 400)

        if password != confirmation:
            return apology("Passwords don't match", 400)

        try:
            hash = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
            rows = db.execute("SELECT id FROM users WHERE username = ?", username)
            session["user_id"] = rows[0]["id"]
            return redirect("/")

        except ValueError:
            return apology("Username already exists", 400)

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "GET":
        rows = db.execute("SELECT symbol FROM portfolio WHERE user_id = ?", session["user_id"])
        symbols = [row["symbol"] for row in rows]

        return render_template("sell.html", symbols=symbols)

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        rows = db.execute("SELECT symbol, shares FROM portfolio WHERE user_id = ?",
                          session["user_id"])

        current_shares = next(row["shares"] for row in rows if row["symbol"] == symbol)

        if not symbol:
            return apology("MISSING SYMBOL", 400)

        if not shares:
            return apology("MISSING SHARES", 400)

        if not any(row["symbol"] == symbol for row in rows):
            return apology("SYMBOL NOT OWNED", 400)

        if shares > current_shares:
            return apology("TOO MANY SHARES", 400)

        quote = lookup(symbol)
        if not quote:
            return apology("INVALID SYMBOL", 400)

        price = quote["price"]
        total_sale = price * shares

        new_shares = current_shares - shares

        if new_shares == 0:
            db.execute("DELETE FROM portfolio WHERE user_id = ? AND symbol = ?",
                       session["user_id"], symbol)
        else:
            db.execute("UPDATE portfolio SET shares = ? WHERE user_id = ? AND symbol = ?",
                       new_shares, session["user_id"], symbol)

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_sale, session["user_id"])

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, type) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], symbol, -shares, price, "SELL")

        return redirect("/")
