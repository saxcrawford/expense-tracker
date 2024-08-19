from flask import Flask, request, render_template, redirect, flash, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import Error
from functools import wraps

app = Flask(__name__)
app.secret_key = 'secret_key'

def create_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Ir0n.mAn2024',
            database='budget_tracker'
        )
        return conn
    except Error as e:
        print(f"Error: '{e}'")
        return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return render_template('login.html')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('dashboard.html')
    return render_template('index.html')

@app.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():
    if request.method == 'POST':
        amount = request.form['transaction_amount']
        description = request.form['transaction_desc']
        date = request.form['transaction_date']
        category_name = request.form['category_name']
        type = request.form['transaction_type']
        conn = create_connection()
        cursor = conn.cursor()
        user_id = session['user_id']

        cursor.execute('SELECT category_id FROM Categories WHERE category_name = %s', (category_name,))
        category_id = cursor.fetchone()
        category_id = category_id[0]

        cursor.execute('INSERT INTO Transactions (transaction_amount, transaction_desc, transaction_date, category_id, transaction_type, user_id) VALUES (%s, %s, %s, %s, %s, %s)', 
                (amount, description, date, category_id, type, user_id))
        conn.commit()
        cursor.close()
        conn.close()
    return render_template('add_transaction.html')

@app.route('/view_transactions', methods=['GET'])
@login_required
def view_transactions():
    user_id = session['user_id']
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
            SELECT t.transaction_id, t.transaction_amount, t.transaction_desc, t.transaction_date, c.category_name, t.transaction_type
            FROM Transactions t
            JOIN Categories c ON t.category_id = c.category_id
            WHERE t.user_id = %s
        ''', (user_id,))
    transactions = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view_transactions.html', transactions=transactions)

@app.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Transactions WHERE transaction_id = %s', (transaction_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('view_transactions.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return render_template('dashboard.html')
    
    try:
        if request.method == 'POST':
            username = request.form['user_username']
            password = request.form['user_password']
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Users (user_username, user_password) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()
            cursor.execute("SELECT * FROM Users WHERE user_username = %s", (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user[2], password):
                session['user_id'] = user[0]
                session['username'] = user[1]
                return render_template('view_transactions.html')
    except Error as e:
        flash('Username already taken')
        return render_template('register.html')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return render_template('dashboard.html')
    
    if request.method == 'POST':
        username = request.form['user_username']
        password = request.form['user_password']
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE user_username = %s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return render_template('dashboard.html')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)