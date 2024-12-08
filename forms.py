from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, DateField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from werkzeug.security import generate_password_hash
from .models import User, Category
from wtforms.validators import ValidationError

# Registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # Custom validation for email uniqueness
    def validate_email(self, email):
        existing_user = User.query.filter_by(email=email.data).first()
        if existing_user:
            raise ValidationError('Email is already in use.')

#Transaction form
class TransactionForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    amount = DecimalField('Amount', places=2, rounding=None, validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Transaction')

    def populate_categories(self, user_id):
        categories = Category.query.filter_by(user_id=user_id).all()
        
        # If categories exist, populate the field with category IDs and names
        if categories:
            self.category_id.choices = [(category.id, category.name) for category in categories]
        else:
            # If no categories exist, set choices to None, so the user can't submit a form without categories
            self.category_id.choices = [(-1, "No categories available")]










