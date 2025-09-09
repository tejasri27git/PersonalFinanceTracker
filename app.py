from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = "finance.db"

# ---------- Database Setup ----------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS incomes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    amount INTEGER NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    amount INTEGER NOT NULL
                )''')
    conn.commit()
    conn.close()

# ---------- Index ----------
@app.route("/")
def home():
    return redirect(url_for('index'))

@app.route("/index")
def index():
    return render_template("index.html")

# ---------- Dashboard ----------
@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT * FROM incomes")
    incomes = c.fetchall()

    c.execute("SELECT * FROM expenses")
    expenses = c.fetchall()

    total_income = sum([row[2] for row in incomes])
    total_expense = sum([row[2] for row in expenses])
    balance = total_income - total_expense

    conn.close()

    return render_template("dashboard.html",
                           incomes=incomes,
                           expenses=expenses,
                           total_income=total_income,
                           total_expense=total_expense,
                           balance=balance)

# ---------- Add Income ----------
@app.route("/add-income", methods=["GET", "POST"])
def add_income():
    if request.method == "POST":
        source = request.form.get("source")
        amount = request.form.get("amount")
        if source and amount:
            try:
                amount = int(amount)
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("INSERT INTO incomes (source, amount) VALUES (?, ?)", (source, amount))
                conn.commit()
                conn.close()
            except ValueError:
                pass
        return redirect(url_for("dashboard"))
    return render_template("add_income.html")

# ---------- Delete Income ----------
@app.route("/delete-income/<int:id>", methods=["POST"])
def delete_income(id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM incomes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("dashboard"))

# ---------- Add Expense ----------
@app.route("/add-expense", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        category = request.form.get("category")
        amount = request.form.get("amount")
        if category and amount:
            try:
                amount = int(amount)
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                # Correct table name: expenses
                c.execute("INSERT INTO expenses (category, amount) VALUES (?, ?)", (category, amount))
                conn.commit()
                conn.close()
            except ValueError:
                pass
        return redirect(url_for("dashboard"))
    return render_template("add_expense.html")

# ---------- Delete Expense ----------
@app.route("/delete-expense/<int:id>", methods=["POST"])
def delete_expense(id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Correct table name: expenses
    c.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("dashboard"))


# ---------- Run ----------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
 
