from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)


conn = sqlite3.connect("bank.bd")


cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    balance REAL NOT NULL
);
""")
conn.commit()

@app.route('/accounts', methods=['GET'])
def get_accounts():
    cursor.execute("SELECT * FROM accounts")
    accounts = cursor.fetchall()
    return jsonify([{'id': account[0], 'name': account[1], 'balance': account[2]} for account in accounts]), 200

@app.route('/account-create', methods=['POST'])
def create_account():
    data = request.get_json()
    name = data.get('name')
    balance = data.get('balance')
    cursor.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, balance))
    conn.commit()
    return jsonify({'message': 'Account created'}), 201


@app.route('/accounts/<int:account_id>', methods=['PUT'])
def update_balance(account_id):
    data = request.get_json()
    balance = data.get('balance')
    cursor.execute("UPDATE accounts SET balance=? WHERE id=?", (balance, account_id))
    conn.commit()
    return jsonify({'message': 'Balance updated'}), 200


@app.route('/deleteAccount/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    cursor.execute("DELETE FROM accounts WHERE id=?", (account_id,))
    conn.commit()

if __name__ == '__main__':
    app.run(debug=True, port=8080)
