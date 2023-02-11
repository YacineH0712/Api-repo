from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
db = SQLAlchemy(app)

class Account(db.Model):
    name = db.Column(db.String, primary_key=True)
    amount = db.Column(db.Integer)
#Default route  
@app.route('/', methods=['GET'])
def home():
   return "<h1>Annuaire Internet</h1> <p API mettant à disposition des données sur les comptes bancaires.</p>"
#Create-account
@app.route('/api/v1/create', methods=["POST"])
def create():
    name = request.json['name']
    amount = request.json['amount']
    account = Account(name=name, amount=amount)
    db.session.add(account)
    db.session.commit()
    return f"Account created for {name} with initial amount of {amount}"

#Get amount of one count by giving his name
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
#To withdraw money from an account
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

#To use the api localy
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
        
       
 #To deploy the api on AWS we must use this app.run command     
 #if __name__ == "__main__":
    #with app.app_context():
        #db.create_all()
        #app.run(debug=True , host='0.0.0.0', port=5000) 
