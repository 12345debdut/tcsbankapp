from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField,IntegerField,DateField,HiddenField,BooleanField
from wtforms.validators import DataRequired,Length,Email,ValidationError
from bank.country_state import state
from bank.models import Customer,CustomerAccount
import datetime
import re
class LoginForm(FlaskForm):
    username=StringField('Username',
        validators=[DataRequired(),Length(min=8)])
    password=PasswordField('Password',
        validators=[DataRequired(),Length(min=6)])
    submit=SubmitField('Log in')
    def validate_password(self,password):
        p=re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&_])[A-Za-z\d@$!%*#?&_]{8,}$")
        m=p.match(password.data)
        if not m:
            raise ValidationError("Please give password in correct format")

class CustomerCreateForm(FlaskForm):
    SSH_id=IntegerField('Customer SSH_ID',validators=[DataRequired()])
    name=StringField('Customer Name',validators=[DataRequired(),Length(min=4)])
    age=IntegerField('Age',validators=[DataRequired()])
    address=StringField('Address',validators=[DataRequired()])
    state=SelectField('State',validators=[DataRequired()],choices=state)
    city=StringField('City',validators=[DataRequired()])
    submit=SubmitField('Create customer')
    def validate_SSH_id(self,SSH_id):
        user=Customer.query.filter_by(SSH_id=SSH_id.data).first()
        if user:
            raise ValidationError("Already SSH_ID exists!!")
        if len(str(SSH_id.data))<6:
            raise ValidationError("SSH ID should be atleast 6 characters!!")

class CustomerUpdateForm(FlaskForm):
    name=StringField('Customer Name',validators=[DataRequired(),Length(min=4)])
    age=IntegerField('Age',validators=[DataRequired()])
    address=StringField('Address',validators=[DataRequired()])
    state=SelectField('State',validators=[DataRequired()],choices=state)
    city=StringField('City',validators=[DataRequired()])
    active=BooleanField('Active',default=False)
    submit=SubmitField('Update customer')
class CustomerAccountCreateForm(FlaskForm):
    customer_id=IntegerField('Customer ID',validators=[DataRequired()])
    account_type=SelectField('Account type',validators=[DataRequired()],choices=[('1','savings'),('2','current')])
    deposit_amount=IntegerField('Initial Deposit',validators=[DataRequired()])
    submit=SubmitField('Create account')
    def validate_customer_id(self,customer_id):
        account=CustomerAccount.query.filter_by(customer_id=customer_id.data).first()
        customer=Customer.query.filter_by(customer_id=customer_id.data).first()
        if account:
            raise ValidationError("Customer already has an account")
        if customer.active==0:
            raise ValidationError("Please activate the account first")

class CustomerSearch(FlaskForm):
    customer_id=IntegerField('Customer ID: ')
    customer_SSH_id=IntegerField('Customer SSH_ID: ')
    submit=SubmitField('Search')
    def validate_customer_id(self,customer_id):
        if customer_id.data !=0:
            customer=Customer.query.filter_by(customer_id=customer_id.data).first()
            if not customer:
                raise ValidationError("Customer does not exist")
    def validate_customer_SSH_id(self,customer_SSH_id):
        if customer_SSH_id.data !=0:
            customer=Customer.query.filter_by(SSH_id=customer_SSH_id.data).first()
            if not customer:
                raise ValidationError("Customer does not exist")

class AccountSearch(FlaskForm):
    account_id=IntegerField('Account ID:')
    customer_id=IntegerField('Customer ID:')
    submit=SubmitField('Search')
    def validate_account_id(self,account_id):
        if account_id.data !=0:
            account=CustomerAccount.query.filter_by(account_id=account_id.data).first()
            if not account:
                raise ValidationError("Please give a valid account id")
    def validate_customer_id(self,customer_id):
        if customer_id.data !=0:
            customer=Customer.query.filter_by(customer_id=customer_id.data).first()
            account=CustomerAccount.query.filter_by(customer_id=customer_id.data).first()
            if customer:
                if not account:
                    raise ValidationError("This customer has no account assosiated with it")
            else:
                raise ValidationError("Customer doesn't exists")
class DepositAmount(FlaskForm):
    amount=IntegerField('Deposit amount',validators=[DataRequired()])
    submit=SubmitField('Deposit')

class WithDrawAmount(FlaskForm):
    amount=IntegerField('Withdraw amount',validators=[DataRequired()])
    submit=SubmitField('Withdraw')
    def validate_amount(self,amount):
        account_id=request.args.get('account_id')
        account=CustomerAccount.query.filter_by(account_id=account_id).first()
        if account.deposit_amount<amount.data:
            raise ValidationError("Please give a sufficient amount to deduct")

class TransferAmount(FlaskForm):
    amount=IntegerField('Transfer amount',validators=[DataRequired()])
    transfer_account=IntegerField('Transfer account no:',validators=[DataRequired()])
    submit=SubmitField('Transfer')
    def validate_amount(self,amount):
        account_id=request.args.get('account_id')
        account=CustomerAccount.query.filter_by(account_id=account_id).first()
        if account.deposit_amount<amount.data:
            raise ValidationError("Please give a sufficient amount to deduct")
    def validate_transfer_account(self,account_id):
        account=CustomerAccount.query.filter_by(account_id=account_id.data).first()
        customer=Customer.query.filter_by(customer_id=account.customer_id).first()
        if customer:
            if customer.active==0:
                raise ValidationError("Please activate the transfer customer account first!!")
        if not account:
            raise ValidationError("Please provide a valid transfer account id")


class FilterTransaction(FlaskForm):
    account_id=IntegerField('Account id',validators=[DataRequired()])
    start_date=DateField('Start Date',format='%Y-%m-%d',validators=[DataRequired()])
    end_date=DateField('End Date',format='%Y-%m-%d',validators=[DataRequired()])
    submit=SubmitField('Search')
    def validate_account_id(self,account_id):
        account=CustomerAccount.query.filter_by(account_id=account_id.data).first()
        if account:
            pass
        else:
            raise ValidationError("The account no. doesn't assosiate with any customer account")
    def validate_start_date(self,start_date):
        if start_date.data>datetime.date.today():
            raise ValidationError("Start date should be less than current date")
    def validate_end_date(self,end_date):
        if end_date.data>datetime.date.today():
            raise ValidationError("Start date should be less than current date")

class GeneratePdf(FlaskForm):
    account_id=HiddenField('Account id',validators=[DataRequired()])
    start_date=HiddenField('Start date',validators=[DataRequired()])
    end_date=HiddenField('End date',validators=[DataRequired()])
    submit=SubmitField('Generate PDF')


    