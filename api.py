from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
db = SQLAlchemy(app)

class Account(db.Model):
    name = db.Column(db.String, primary_key=True)
    amount = db.Column(db.Integer)

@app.route('/api/v1/create', methods=["POST"])
def create():
    name = request.json['name']
    amount = request.json['amount']
    account = Account(name=name, amount=amount)
    db.session.add(account)
    db.session.commit()
    return f"Account created for {name} with initial amount of {amount}"

@app.route('/api/v1/amount', methods=["GET"])
def amount():
    name = request.args.get('name')
    account = Account.query.get(name)
    if account:
        return str(account.amount)
    else:
        return "No account found with the name " + name

@app.route("/api/v1/deposit", methods=["POST"])
def deposit():
    name = request.json['name']
    amount = request.json['amount']
    account = Account.query.get(name)
    if account:
        account.amount += amount
        db.session.commit()
        return f"Deposited {amount} to the account of {name}"
    else:
        return "No account found with the name " + name

@app.route("/api/v1/withdraw", methods=["POST"])
def withdraw():
    name = request.json['name']
    amount = request.json['amount']
    account = Account.query.get(name)
    if account:
        if amount > account.amount:
            return f"Insufficient amount in the account of {name}"
        else:
            account.amount -= amount
            db.session.commit()
            return f"Withdrew {amount} from the account of {name}"
    else:
        return "No account found with the name " + name

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
