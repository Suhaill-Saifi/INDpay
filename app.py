import os
import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, render_template, flash, redirect, url_for, session, request
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from functools import wraps
from forms import RegisterForm, SendMoneyForm, BuyForm
from sqlhelpers import get_blockchain as _get_blockchain, sync_blockchain as _sync_blockchain

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'secret123')

# MySQL config from environment variables (set in docker-compose.yml)
app.config['MYSQL_HOST']        = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER']        = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD']    = os.environ.get('MYSQL_PASSWORD', '')
app.config['MYSQL_DB']          = os.environ.get('MYSQL_DB', 'INDpay')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


# ── Auth decorator ──────────────────────────────────────────────────────────
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        flash("Unauthorized, please login.", "danger")
        return redirect(url_for('login'))
    return wrap


# ── Money transfer helper ───────────────────────────────────────────────────
def send_money(sender, receiver, amount):
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        raise Exception("Invalid amount.")

    if amount <= 0:
        raise Exception("Amount must be greater than zero.")

    cursor = mysql.connection.cursor()
    try:
        # Check sender balance (skip for BANK)
        if sender != "BANK":
            cursor.execute("SELECT balance FROM users WHERE username = %s", [sender])
            row = cursor.fetchone()
            if not row:
                raise Exception("Sender account not found.")
            sender_balance = float(row['balance'])
            if sender_balance < amount:
                raise Exception(f"Insufficient balance. You have {sender_balance:.2f} IND but tried to send {amount:.2f} IND.")

        # Check receiver exists
        cursor.execute("SELECT id FROM users WHERE username = %s", [receiver])
        if not cursor.fetchone():
            raise Exception(f"User '{receiver}' does not exist.")

        if sender == receiver:
            raise Exception("Cannot send money to yourself.")

        # Update balances
        if sender != "BANK":
            cursor.execute(
                "UPDATE users SET balance = balance - %s WHERE username = %s",
                (amount, sender)
            )
        cursor.execute(
            "UPDATE users SET balance = balance + %s WHERE username = %s",
            (amount, receiver)
        )

        # Record in transactions table
        cursor.execute(
            "INSERT INTO transactions (sender, receiver, amount) VALUES (%s, %s, %s)",
            (sender, receiver, amount)
        )
        mysql.connection.commit()

        # Record in blockchain
        try:
            from blockchain import Block
            blockchain = _get_blockchain(mysql)
            block_number = len(blockchain.chain) + 1
            block_data   = f"{sender}-->{receiver}-->{amount}"
            blockchain.mine(Block(block_number, data=block_data))
            _sync_blockchain(mysql, blockchain)
        except Exception as bc_err:
            # Blockchain failure should not roll back the financial transaction
            app.logger.warning(f"Blockchain sync failed: {bc_err}")

    except Exception:
        mysql.connection.rollback()
        raise
    finally:
        cursor.close()


# ── Routes ──────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if not form.validate():
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{field}: {error}", 'danger')
            return render_template('register.html', form=form)
        username = form.username.data
        cursor   = mysql.connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", [username])
        if cursor.fetchone():
            cursor.close()
            flash('Username already taken', 'danger')
            return redirect(url_for('register'))
        cursor.close()

        password = sha256_crypt.encrypt(form.password.data)
        cursor   = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, username, password, balance) VALUES (%s,%s,%s,%s,%s)",
            (form.name.data, form.email.data, username, password, 1000.00)
        )
        mysql.connection.commit()
        cursor.close()

        session['logged_in'] = True
        session['username']  = username
        session['name']      = form.name.data
        session['email']     = form.email.data
        flash('Registration successful. Welcome!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username  = request.form['username']
        candidate = request.form['password']
        cursor    = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", [username])
        user = cursor.fetchone()
        cursor.close()

        if user and sha256_crypt.verify(candidate, user['password']):
            session['logged_in'] = True
            session['username']  = username
            session['name']      = user.get('name', username)
            session['email']     = user.get('email', '')
            flash('You are now logged in.', 'success')
            return redirect(url_for('dashboard'))

        flash('Invalid username or password', 'danger')
    return render_template('login.html')


@app.route("/logout")
@is_logged_in
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))


@app.route("/dashboard")
@is_logged_in
def dashboard():
    from datetime import datetime
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", [session['username']])
    user_data = cursor.fetchone()
    balance   = user_data['balance'] if user_data else 0

    cursor.execute(
        "SELECT * FROM transactions WHERE sender=%s OR receiver=%s ORDER BY timestamp DESC LIMIT 10",
        [session['username'], session['username']]
    )
    transactions = cursor.fetchall()

    cursor.execute("SELECT * FROM users")
    all_users = cursor.fetchall()
    cursor.close()

    try:
        blockchain = _get_blockchain(mysql).chain
    except Exception:
        blockchain = []

    return render_template('dashboard.html',
                           balance=balance,
                           transactions=transactions,
                           data=all_users,
                           blockchain=blockchain,
                           ct=datetime.now().strftime("%H:%M"))


@app.route("/transection", methods=['GET', 'POST'])
@is_logged_in
def transection():
    form   = SendMoneyForm(request.form)
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT balance FROM users WHERE username = %s", [session['username']])
    row    = cursor.fetchone()
    cursor.close()
    balance = row['balance'] if row else 0

    if request.method == 'POST':
        if not form.validate():
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{error}", 'danger')
        else:
            try:
                send_money(session['username'], form.username.data, form.amount.data)
                flash("Money sent successfully!", "success")
            except Exception as e:
                flash(str(e), 'danger')
        return redirect(url_for('transection'))

    return render_template('transection.html', balance=balance, form=form, page='transection')


@app.route("/buy", methods=['GET', 'POST'])
@is_logged_in
def buy():
    form   = BuyForm(request.form)
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT balance FROM users WHERE username = %s", [session['username']])
    row    = cursor.fetchone()
    cursor.close()
    balance = row['balance'] if row else 0

    if request.method == 'POST':
        if not form.validate():
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{error}", 'danger')
        else:
            try:
                send_money("BANK", session['username'], form.amount.data)
                flash("Purchase successful! Funds added to your account.", "success")
            except Exception as e:
                flash(str(e), 'danger')
        return redirect(url_for('dashboard'))

    return render_template('buy.html', balance=balance, form=form, page='buy')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
