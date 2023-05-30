from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm 
from sqlalchemy_utils import PhoneNumberType
from wtforms import StringField
import os
from wtforms.validators import Length, DataRequired

application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guest.db'

db = SQLAlchemy(application)

SECRET_KEY = os.urandom(32)
application.config['SECRET_KEY'] = SECRET_KEY

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150),  nullable=False)
    number = db.Column(PhoneNumberType(region="RU"), nullable=False)
    is_kid = db.Column(db.Boolean)

    def __repr__(self):
        return f'{self.name} | {self.number}'
    
class GuestForm(FlaskForm):
    name = StringField(validators=[Length(max=150)], render_kw={"placeholder": "Введите ФИО"})
    phone = StringField(validators=[DataRequired()], render_kw={"placeholder": "Введите номер телефона"})

@application.route('/', methods=['POST', 'GET'])
def main():
    form = GuestForm() 
    if request.method == 'POST':
        names = request.form.getlist('name[]')
        phone = request.form.getlist('phone')
        
        for i,name in enumerate(names): 
            guest = Guest(name=name, number=phone[0], is_kid=False)
            db.session.add(guest)
            db.session.commit()
    return render_template('test2.html', form=form)


@application.route("/get_guests", methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return render_template('guests.html', guests=guests)

@application.route("/guest/<int:id>/delete/")
def delete_guest(id):
    guest_del = Guest.query.get_or_404(id)
    try:
        db.session.delete(guest_del)
        db.session.commit()
        return redirect("/get_guests")
    except:
        return "ПРи удалении произошла ошибка!"



if __name__ == "__main__":
    application.run(debug=True)