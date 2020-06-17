from bank import db,login_manager
from sqlalchemy import Column,Integer,String,Boolean
from flask_login import UserMixin
import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    password=db.Column(db.String(120),unique=True,nullable=False)
    is_customer_exec=db.Column(db.Boolean,nullable=True)
    is_teller=db.Column(db.Boolean,nullable=True)
    is_cashier=db.Column(db.Boolean,nullable=True)
    def __repr__(self):
        return f'Username: {self.username}'

class Customer(db.Model):
    customer_id=db.Column(db.Integer,primary_key=True,nullable=False)
    SSH_id=db.Column(db.Integer,nullable=False)
    name=db.Column(db.String(50),nullable=False)
    age=db.Column(db.Integer,nullable=False)
    address=db.Column(db.String(120),nullable=False)
    state=db.Column(db.String(50),nullable=False)
    city=db.Column(db.String(50),nullable=False)
    active=db.Column(db.Boolean,nullable=False)
    message=db.Column(db.String(200),nullable=False)
    last_updated=db.Column(db.DateTime,nullable=False,default=datetime.datetime.now)

    # def __init__(self,customer_id,SSH_id,name,age,address,state,city,active,message,last_updated):
    #     self.customer_id=customer_id
    #     self.SSH_id=SSH_id
    #     self.name=name
    #     self.age=age
    #     self.address=address
    #     self.state=state
    #     self.city=city
    #     self.active=active
    #     self.message=message
    #     self.last_updated=last_updated


class CustomerAccount(db.Model):
    account_id=db.Column(db.Integer,primary_key=True,nullable=False)
    customer_id=db.Column(db.Integer,db.ForeignKey('customer.customer_id'),nullable=False)
    customer = db.relationship("Customer", backref=db.backref("customer", uselist=False))
    account_type=db.Column(db.String(30),nullable=False)
    deposit_amount=db.Column(db.Integer,nullable=False)
    last_updated=db.Column(db.DateTime,nullable=False,default=datetime.datetime.now)

    def __repr__(self):
        return f'Account: {self.account_id} Customer_id: {self.customer_id}'

class TransactionInfo(db.Model):
    transaction_id=db.Column(db.String(100),primary_key=True,nullable=False)
    account_id=db.Column(db.Integer,db.ForeignKey('customer_account.account_id'),nullable=False)
    account = db.relationship("CustomerAccount", backref=db.backref("customer_account", uselist=False))
    amount=db.Column(db.Integer,nullable=False)
    deposit=db.Column(db.Boolean,nullable=False)
    transfer=db.Column(db.Boolean,nullable=False)
    transfer_account_id=db.Column(db.Integer,nullable=False)
    action_date=db.Column(db.DateTime,nullable=False,default=datetime.datetime.now)