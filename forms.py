from typing import Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,BooleanField,ValidationError,validators,IntegerField,TextField
from wtforms.validators import DataRequired,EqualTo,Length

#register form
class register(FlaskForm):
    fname=StringField('First_Name',validators=[DataRequired()])
    lname=StringField('Last_Name',validators=[DataRequired()])
    email=StringField('Email',validators=[DataRequired()])
    password=StringField('Password',validators=[DataRequired()])
    reg=SubmitField('Register')
#Singin Form
class singin(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    sing_in = SubmitField('Sign In')

#Bill Payment Form
class bill_pay(FlaskForm):
    name = StringField('Payee Name',validators=[DataRequired()])
    amount = IntegerField('Amount',validators=[DataRequired()])
    submit = SubmitField('Done')

class transfer_pay(FlaskForm):
    withdraw = StringField('Credit Card',validators=[DataRequired()])
    to = StringField('Account No',validators=[DataRequired()])
    amount = IntegerField('Amount',validators=[DataRequired()])
    submit = SubmitField('Done')

class e_tran_pay(FlaskForm):
    withdraw= StringField('Enter Recivers Email-Id',validators=[DataRequired()])
    contact= StringField('Enter Sender  Email-Id',validators=[DataRequired()])
    amount = IntegerField('Amount',validators=[DataRequired()])
    submit = SubmitField('Done')
class contact(FlaskForm):
    fname=StringField('First_Name',validators=[DataRequired()])
    lname=StringField('Last_Name',validators=[DataRequired()])
    p = TextField('Please Explain your Problem')
    reg=SubmitField('Register')