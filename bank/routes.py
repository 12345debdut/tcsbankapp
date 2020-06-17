from flask import render_template
from bank import app
from bank.decorator import customer_executive_required,cashier_teller_required
from bank.views.auth.index import login_view,logout_view
from bank.views.customer.index import create_customer_view,all_customer_view,edit_customer_view,delete_customer_view,customer_details_view,refresh_api
from bank.views.customer.search import customer_search_view,single_customer_view
from bank.views.account.index import create_account_view,account_status_view,delete_account_view,single_account_view,account_search_view
from bank.views.account.transaction import deposit_account_view,withdraw_account_view,transfer_account_view
from bank.views.transaction.index import all_transaction_view,filter_transaction_view
from bank.views.transaction.physicalcopy import generate_pdf_view,generate_excel_view


@app.route('/')
def index():
    return render_template("index.html",title="Home page")

# login route
@app.route('/login',methods=['GET','POST'])
def login():
    return login_view()

@app.route('/logout')
def logout():
    return logout_view()

@app.route('/create/customer',methods=['GET','POST'])
@customer_executive_required
def create_customer():
    return create_customer_view()

@app.route('/api/customer/refresh')
@customer_executive_required
def refresh_customer():
    return refresh_api()

@app.route('/all/customer')
@customer_executive_required
def all_customer():
    return all_customer_view()

@app.route('/customer/details')
@customer_executive_required
def customer_details():
    return customer_details_view()


@app.route('/edit/customer',methods=['GET','POST'])
@customer_executive_required
def edit_customer():
    return edit_customer_view()

@app.route('/delete/customer')
@customer_executive_required
def delete_customer(): 
    return delete_customer_view()

@app.route('/single/customer')
@customer_executive_required
def single_customer():
    return single_customer_view()

@app.route('/search/customer',methods=['GET','POST'])
@customer_executive_required
def customer_search():
    return customer_search_view()

@app.route('/create/account',methods=['GET','POST'])
@customer_executive_required
def create_account():
    return create_account_view()

@app.route('/account/status')
@customer_executive_required
def account_status():
    return account_status_view()

@app.route('/delete/account')
@customer_executive_required
def delete_account():
    return delete_account_view()

@app.route('/single/account')
@cashier_teller_required
def single_account():
    return single_account_view()

@app.route('/account/search',methods=['GET','POST'])
@cashier_teller_required
def account_search():
    return account_search_view()

@app.route('/deposit/account',methods=['GET','POST'])
@cashier_teller_required
def deposit_account():
    return deposit_account_view()

@app.route('/withdraw/account',methods=['GET','POST'])
@cashier_teller_required
def withdraw_account():
    return withdraw_account_view() 

@app.route('/transfer/money',methods=['GET','POST'])
@cashier_teller_required
def transfer_account():
    return transfer_account_view()

@app.route('/all/transaction')
@cashier_teller_required
def all_transaction():
    return all_transaction_view()


@app.route('/filter/transaction',methods=['GET','POST'])
@cashier_teller_required
def filter_transaction():
    return filter_transaction_view()

@app.route('/generate/pdf/<string:start_date>/<string:end_date>')
@cashier_teller_required
def generate_pdf(start_date,end_date):
    return generate_pdf_view(start_date=start_date,end_date=end_date)

@app.route('/generate/excel/<string:start_date>/<string:end_date>')
@cashier_teller_required
def generate_excel(start_date,end_date):
    return generate_excel_view(start_date=start_date,end_date=end_date)