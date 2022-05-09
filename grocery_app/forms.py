from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL
from grocery_app.extensions import app, db
from .models import ItemCategory, GroceryStore, User

item_catagories = ItemCategory

class GroceryStoreForm(FlaskForm):
    title = StringField("Store Name: ", validators=[DataRequired()])
    address = StringField("Store Address: ", validators=[DataRequired()])
    submit = SubmitField("Submit")

class GroceryItemForm(FlaskForm):
    name = StringField("Item: ", validators=[DataRequired()])
    price = FloatField("Price: ", validators=[DataRequired()])
    category = SelectField(u'Category: ', choices=item_catagories)
    photo_url = StringField("Photo URL: ")
    store = SelectField(u'Store', choices = [(store.id, store.title) for store in GroceryStore.query.all()])
    submit = SubmitField("Submit")

class SignUpForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('No user with that username. Please try again.')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password doesn\'t match. Please try again.')