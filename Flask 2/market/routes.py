from market import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from market.models import Item, User
from market.forms import RegisterForm, LoginForm
from market import db
from flask_login import login_user

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/market')
def market_page():
    """
    with app.app_context():
        for item in items:
            # Avoid duplicates
            if not Item.query.filter_by(name=item["name"]).first():
                new_item = Item(
                    name=item["name"],
                    barcode=item["barcode"],
                    price=item["price"],
                    description=f'Description for {item["name"]}'
                )
                db.session.add(new_item)
                db.session.commit()
                print(f'{item["name"]} has been added successfully')
                """
    db_items = Item.query.all()
    return render_template('market.html', items=db_items)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        with app.app_context():
            db.session.add(user_to_create)
            db.session.commit()
            return redirect(url_for('market_page'))
    if form.errors != {}: # If there are no errorse from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error in creating the user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
            ):
                login_user(attempted_user)
                flash(f"Success! You are logged in as: {attempted_user.username}", category="success")
                return redirect(url_for('market_page'))
        else:
            flash('Username and Password are incorrect! Try again', category="danger")

    return render_template('login.html', form=form)