from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem
from grocery_app.forms import GroceryStoreForm, GroceryItemForm

# Import app and db from events_app package so that we can run app
from grocery_app.extensions import app, db
from flask_login import login_required, login_user, logout_user, current_user

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    print(all_stores)
    return render_template('home.html', all_stores=all_stores)

@login_required
@main.route('/new_store', methods=['GET', 'POST'])
def new_store():
    form = GroceryStoreForm()
    if request.method == 'POST':
      store_title = request.form.get('title')
      store_address = request.form.get('address')
      store = GroceryStore(
          title = store_title,
          address = store_address,
          created_by = current_user,
      )
      db.session.add(store)
      db.session.commit()
      return redirect(url_for('main.store_detail', store_id = store.id))
    else:
      return render_template('new_store.html', form=form)

@login_required
@main.route('/new_item', methods=['GET', 'POST'])
def new_item():
    form = GroceryItemForm()
    if request.method == 'POST':
        item_name = request.form.get('name')
        item_price = request.form.get('price')
        item_category = request.form.get('category')
        item_photo_url = request.form.get('photo_url')
        item_store = request.form.get('store')
        item = GroceryItem(
            name = item_name,
            price = item_price,
            category = item_category,
            photo_url = item_photo_url,
            store_id = item_store,
            created_by = current_user,
        )
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('main.item_detail', item_id=item.id))
    else: 
        return render_template('new_item.html', form=form)

@login_required
@main.route('/store/<store_id>', methods=['GET', 'POST'])
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)
    form = GroceryStoreForm(obj=store)
    if request.method == 'POST':
        store.title = request.form.get('title')
        store.address = request.form.get('address')
        db.session.commit()
        return redirect(url_for('main.store_detail', store_id = store.id))
    else:
        return render_template('store_detail.html', store=store, form=form)

@login_required
@main.route('/item/<item_id>', methods=['GET', 'POST'])
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)
    form = GroceryItemForm(obj=item)
    if request.method == 'POST':
        item.name = request.form.get('name')
        item.price = request.form.get('price')
        item.category = request.form.get('category').upper()
        item.photo_url = request.form.get('photo_url')
        item.store_id = request.form.get('store')
        db.session.commit()
        return redirect(url_for('main.item_detail', item_id = item.id))
    item = GroceryItem.query.get(item_id)
    return render_template('item_detail.html', item=item, form=form)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            password=form.username.password
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))