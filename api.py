from flask import Flask, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    return sqlite3.connect("bank.db")

@app.route('/api/v1/create', methods=["POST"])
def create():
    conn = get_db_connection()
    c = conn.cursor()
    name = request.json['name']
    amount = request.json['amount']
    c.execute("INSERT INTO accounts (name, amount) VALUES (?,?)", (name, amount))
    conn.commit()
    conn.close()
    return f"Account created for {name} with initial amount of {amount}"

@app.route('/api/v1/amount', methods=["GET"])
def amount():
    conn = get_db_connection()
    c = conn.cursor()
    name = request.args.get('name')
    c.execute("SELECT amount FROM accounts WHERE name=?", (name,))
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
    name = request.json['name']
    amount = request.json['amount']
    c.execute("UPDATE accounts SET amount = amount + ? WHERE name = ?", (amount, name))
    conn.commit()
    conn.close()
    return f"Deposited {amount} to the account of {name}"

@app.route("/api/v1/withdraw", methods=["POST"])
def withdraw():
    conn = get_db_connection()
    c = conn.cursor()
    name = request.json['name']
    amount = request.json['amount']
    c.execute("SELECT amount FROM accounts WHERE name = ?", (name,))
    result = c.fetchone()
    if result:
        current_amount = result[0]
        if amount > current_amount:
            return f"Insufficient amount in the account of {name}"
        else:
            c.execute("UPDATE accounts SET amount = amount - ? WHERE name = ?", (amount, name))
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
            amount INTEGER 
        )
    """)
    conn.commit()
    conn.close()
    app.run(debug=True)
