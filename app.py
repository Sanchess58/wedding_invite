import os

from flask import Flask, redirect, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy_utils import PhoneNumberType
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length
from flask_login import login_required, UserMixin, LoginManager, login_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guest.db'

db = SQLAlchemy(app)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/'

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150),  nullable=False)
    number = db.Column(PhoneNumberType(region="RU"), nullable=False)

    def __repr__(self):
        return f'{self.name} | {self.number}'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150),  nullable=False)
    password = db.Column(db.String(100))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class GuestForm(FlaskForm):
    name = StringField(
        validators=[Length(max=150)],
        render_kw={"placeholder": "Введите ФИО"}
    )
    phone = StringField(
        validators=[DataRequired()],
        render_kw={"placeholder": "Введите номер телефона"}
    )

class UserForm(FlaskForm):
    name = StringField(
        validators=[Length(max=150)],
        render_kw={"placeholder": "Введите username"}
    )
    password = PasswordField(
        validators=[DataRequired(), Length(min=8)],
        render_kw={"placeholder": "Введите пароль"}
    )


@app.route('/', methods=['POST', 'GET'])
def main():
    form = GuestForm()
    if request.method == 'POST':
        names = request.form.getlist('name[]')
        phone = request.form.getlist('phone')

        for name in names:
            guest = Guest(name=name, number=phone[0])
            db.session.add(guest)
            db.session.commit()
    return render_template('test2.html', form=form)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    button = "Зарегистрироваться"
    text_sign_login = "Регистрация"
    form = UserForm()
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        new_user = User(name=name, password=generate_password_hash(password, method='scrypt'))
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    return render_template('signup.html', form=form, button=button, text_sign_login=text_sign_login)



@app.route('/login', methods=['POST', 'GET'])
def login():
    button = "Войти"
    text_sign_login = "Авторизация"
    form = UserForm()
    if request.method == "POST":
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(name=name).first()
        if not user or not check_password_hash(user.password, password):
            flash("Введены неверные данные")
            return redirect('/login')
        login_user(user, remember=True)
        return redirect('/get_guests')
    return render_template('signup.html', form=form, button=button, text_sign_login=text_sign_login)


@app.route("/get_guests", methods=['GET'])
@login_required
def get_guests():
    guests = Guest.query.all()
    return render_template('guests.html', guests=guests)


@app.route("/guest/<int:id>/delete/")
@login_required
def delete_guest(id):
    guest_del = Guest.query.get_or_404(id)
    try:
        db.session.delete(guest_del)
        db.session.commit()
        return redirect("/get_guests")
    except Exception as e:
        return f"При удалении произошла ошибка! {e}"


if __name__ == "__main__":
    app.run(debug=True)