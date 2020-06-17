from flask import redirect,url_for,request,flash
from flask_login import current_user
from bank.models import Customer,CustomerAccount
from functools import wraps
def customer_executive_required(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if current_user.is_authenticated:
            if current_user.is_customer_exec==1:
                return func(*args,**kwargs)
            else:
                return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    return inner

def cashier_teller_required(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if current_user.is_authenticated:
            if current_user.is_cashier==1 or current_user.is_teller==1:
                return func(*args,**kwargs)
            else:
                return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    return inner

def customer_activation_required(func):
    @wraps(func)
    def inner(*args,**kwargs):
        try:
            account_id=request.args.get('account_id',None)
            account=CustomerAccount.query.filter_by(account_id=account_id).first()
            if not account:
                flash('Please provide valid account id')
                return redirect(url_for("index"))
            customer_id=account.customer.customer_id
            if account.customer.active==1:
                return func(*args,**kwargs)
            else:
                flash(f'Please activate the customer account {customer_id}','danger')
                return redirect(url_for('index'))
        except Exception as e:
            print(e)
            flash('Internal server error')
            return redirect(url_for('index'))
    return inner