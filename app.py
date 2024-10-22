from urllib import request
from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        return redirect(url_for('dashboard'))
    return render_template('add_transaction.html')

@app.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        return redirect(url_for('dashboard'))
    return render_template('edit_transaction.html', transaction_id=transaction_id)

@app.route('/manage_categories', methods=['GET', 'POST'])
def manage_categories():
    if request.method == 'POST':
        category = request.form['category']
        return redirect(url_for('manage_categories'))
    return render_template('manage_categories.html')

@app.route('/reports', methods=['GET', 'POST'])
def reports():
    if request.method == 'POST':
        report_type = request.form['report_type']
        return redirect(url_for('reports'))
    return render_template('reports.html')

if __name__ == '__main__':
    app.run(app.run(debug=True, 
         host='0.0.0.0', 
         port=9000, 
         threaded=True))