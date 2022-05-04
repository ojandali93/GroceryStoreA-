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
    submit = SubmitField("Submit")