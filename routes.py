from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, Transaction, Category
from .forms import RegistrationForm, TransactionForm  # Import the TransactionForm

main = Blueprint('main', __name__)

# 1. Home Page
@main.route('/')
def home():
    return render_template('home.html')

# 2. User Registration
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Hash the password using werkzeug
        hashed_password = generate_password_hash(form.password.data)

        # Create new user
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_password
        )

        # Add to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)

# 3. User Login
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html')

# 4. User Logout
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

# 5. Dashboard
@main.route('/dashboard')
@login_required
def dashboard():
    # Get transactions of the logged-in user
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).limit(5).all()

    # Calculate total income and expenses
    total_income = sum(t.amount for t in transactions if t.amount > 0)
    total_expenses = sum(t.amount for t in transactions if t.amount < 0)

    # Calculate remaining budget 

    remaining_budget = total_income + total_expenses

    return render_template('dashboard.html', 
                           transactions=transactions, 
                           total_income=total_income, 
                           total_expenses=total_expenses, 
                           remaining_budget=remaining_budget)


# 6. Add Transaction
@main.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():
    form = TransactionForm()
    form.populate_categories(current_user.id)  # Populate categories for the current user

    if form.validate_on_submit():
        description = form.description.data
        amount = form.amount.data
        date = form.date.data
        category_id = form.category_id.data

        # Validate category_id (ensure it's not the placeholder -1)
        if category_id == -1:
            flash("Please select a valid category.", 'danger')
            return render_template('add_transaction.html', form=form)

        # Create new transaction if category_id is valid
        new_transaction = Transaction(
            description=description,
            amount=float(amount),
            date=date,
            user_id=current_user.id,
            category_id=category_id
        )
        db.session.add(new_transaction)
        db.session.commit()
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('add_transaction.html', form=form)



# 7. Edit Transaction
@main.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    form = TransactionForm(obj=transaction)  # Populate the form with existing data

    if form.validate_on_submit():
        # Update the transaction with the form data
        transaction.description = form.description.data
        transaction.amount = float(form.amount.data)
        transaction.date = form.date.data
        transaction.category_id = form.category_id.data

        db.session.commit()
        flash('Transaction updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('edit_transaction.html', form=form, transaction=transaction, categories=categories)

# 8. Delete Transaction
@main.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)

    db.session.delete(transaction)
    db.session.commit()
    flash('Transaction deleted successfully!', 'success')
    return redirect(url_for('main.dashboard'))

# 9. Manage Categories
@main.route('/manage_categories', methods=['GET', 'POST'])
@login_required
def manage_categories():
    if request.method == 'POST':
        name = request.form['name']
        # Ensure the category is added correctly with the user's ID
        new_category = Category(name=name, user_id=current_user.id)
        db.session.add(new_category)
        db.session.commit()
        flash('Category added successfully!', 'success')
        return redirect(url_for('main.manage_categories'))

    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('manage_categories.html', categories=categories)


# 10. Delete Category
@main.route('/delete_category/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)

    # First, delete all transactions related to this category
    for transaction in category.transactions:
        db.session.delete(transaction)
    
    # Then delete the category itself
    db.session.delete(category)
    db.session.commit()
    
    flash('Category and its associated transactions deleted successfully!', 'success')
    return redirect(url_for('main.manage_categories'))



# 11. Reports
@main.route('/reports', methods=['GET', 'POST'])
@login_required
def reports():
    start_date = request.args.get('start_date')  # Query params for date range
    end_date = request.args.get('end_date')
    category_id = request.args.get('category_id')

    query = Transaction.query.filter_by(user_id=current_user.id)

    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    if category_id:
        query = query.filter(Transaction.category_id == category_id)

    transactions = query.all()

    # Fetch categories for the filter dropdown
    categories = Category.query.filter_by(user_id=current_user.id).all()

    return render_template('reports.html', transactions=transactions, categories=categories)


