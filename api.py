from flask import Flask, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    return sqlite3.connect("bank.db")

@app.route("/api/v1/create", methods=["POST"])
def create():
    conn = get_db_connection()
    c = conn.cursor()
    name = request.form.get("name")
    balance = request.form.get("balance")
    c.execute("INSERT INTO accounts (name, balance) VALUES (?,?)", (name, balance))
    conn.commit()
    conn.close()
    return f"Account created for {name} with initial balance of {balance}"

@app.route("/api/v1/balance/<name>", methods=["GET"])
def balance(name):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT balance FROM accounts WHERE name=?", (name,))
    result = c.fetchone()
    conn.close()
    if result:
        return str(result[0])
    else:
        return "No account found with the name " + name

@app.route("/api/v1/deposit", methods=["POST"])
def deposit():
    conn = get_db_connection()
    c = conn.cursor()
    name = request.form.get("name")
    amount = request.form.get("amount")
    c.execute("UPDATE accounts SET balance = balance + ? WHERE name = ?", (amount, name))
    conn.commit()
    conn.close()
    return f"Deposited {amount} to the account of {name}"

@app.route("/api/v1/withdraw", methods=["POST"])
def withdraw():
    conn = get_db_connection()
    c = conn.cursor()
    name = request.form.get("name")
    amount = request.form.get("amount")
    c.execute("SELECT balance FROM accounts WHERE name = ?", (name,))
    result = c.fetchone()
    if result:
        current_balance = result[0]
        if amount > current_balance:
            return f"Insufficient balance in the account of {name}"
        else:
            c.execute("UPDATE accounts SET balance = balance - ? WHERE name = ?", (amount, name))
            conn.commit()
            conn.close()
            return f"Withdrew {amount} from the account of {name}"
    else:
        conn.close()
        return "No account found with the name " + name

if __name__ == "__main__":
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            name TEXT PRIMARY KEY,
            balance INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    app.run(debug=True)
