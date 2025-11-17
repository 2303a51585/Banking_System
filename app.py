from flask import Flask, render_template, request, redirect, url_for, session, flash
from user_db import create_user, verify_user, get_user, update_user
from models import SavingsAccount, CurrentAccount, transfer, Transaction
import json

app = Flask(__name__)
app.secret_key = "dev-secret-key"  # for demo only

@app.route('/')
def index():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fullname = request.form.get('fullname','')
        try:
            create_user(username, password, fullname)
            flash("Account created. Please login.")
            return redirect(url_for('login'))
        except Exception as e:
            flash(str(e))
    return render_template("register.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out")
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = get_user(session['username'])
    return render_template("dashboard.html", user=user)

@app.route('/deposit/<acc_type>', methods=['POST'])
def deposit(acc_type):
    if 'username' not in session:
        return redirect(url_for('login'))
    user = get_user(session['username'])
    amount = float(request.form['amount'])
    acc = user['accounts'].get(acc_type)
    if not acc:
        flash("Account not found")
        return redirect(url_for('dashboard'))
    # perform deposit
    # rebuild object
    if acc['acc_type'] == 'savings':
        account = SavingsAccount(**acc)
    else:
        account = CurrentAccount(**acc)
    account.deposit(amount)
    user['accounts'][acc_type] = account.to_dict()
    update_user(session['username'], user)
    flash("Deposit successful")
    return redirect(url_for('dashboard'))

@app.route('/withdraw/<acc_type>', methods=['POST'])
def withdraw(acc_type):
    if 'username' not in session:
        return redirect(url_for('login'))
    user = get_user(session['username'])
    amount = float(request.form['amount'])
    acc = user['accounts'].get(acc_type)
    if not acc:
        flash("Account not found")
        return redirect(url_for('dashboard'))
    if acc['acc_type'] == 'savings':
        account = SavingsAccount(**acc)
    else:
        account = CurrentAccount(**acc)
    try:
        account.withdraw(amount)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('dashboard'))
    user['accounts'][acc_type] = account.to_dict()
    update_user(session['username'], user)
    flash("Withdrawal successful")
    return redirect(url_for('dashboard'))

@app.route('/transfer', methods=['GET','POST'])
def do_transfer():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = get_user(session['username'])
    if request.method == 'POST':
        src = request.form['src']
        dst = request.form['dst']
        amount = float(request.form['amount'])
        # only allow transfers between same user's accounts for demo
        src_acc = user['accounts'][src]
        dst_acc = user['accounts'][dst]
        # rebuild objects
        src_obj = SavingsAccount(**src_acc) if src_acc['acc_type']=='savings' else CurrentAccount(**src_acc)
        dst_obj = SavingsAccount(**dst_acc) if dst_acc['acc_type']=='savings' else CurrentAccount(**dst_acc)
        try:
            transfer(src_obj, dst_obj, amount)
        except Exception as e:
            flash(str(e))
            return redirect(url_for('do_transfer'))
        user['accounts'][src] = src_obj.to_dict()
        user['accounts'][dst] = dst_obj.to_dict()
        update_user(session['username'], user)
        flash("Transfer completed")
        return redirect(url_for('dashboard'))
    return render_template("transfer.html", user=user)

@app.route('/apply_interest', methods=['POST'])
def apply_interest():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = get_user(session['username'])
    months = int(request.form.get('months', 1))
    sav = user['accounts']['savings']
    sav_obj = SavingsAccount(**sav)
    t = sav_obj.apply_interest(months=months)
    user['accounts']['savings'] = sav_obj.to_dict()
    update_user(session['username'], user)
    flash("Interest applied" if t else "No interest to apply")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
