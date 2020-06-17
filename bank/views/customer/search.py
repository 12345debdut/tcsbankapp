from flask import flash,redirect,render_template,url_for,request
from bank import db
from bank.models import Customer
from bank.forms import CustomerSearch
def single_customer_view():
    try:
        id=request.args.get('id',None)
        filter_by=request.args.get('filter_by',None)
        customer=None
        if id and filter_by:
            if filter_by=="customer_id":
                customer=Customer.query.filter_by(customer_id=id).first()
            elif filter_by=="customer_SSH_id":
                customer=Customer.query.filter_by(SSH_id=id).first()
            else:
                redirect(url_for('index'))
        else:
            redirect(url_for('index'))
        return render_template('customer/singlecustomer.html',customer=customer,title="Customer details",filter_by=filter_by)
    except Exception as e:
        flash('Internal server error','danger')
        return redirect(url_for('index'))

def customer_search_view():
    try:
        form=CustomerSearch()
        if form.validate_on_submit():
            id=None
            filter_by=""
            if int(form.customer_id.data)>0:
                id=form.customer_id.data
                filter_by="customer_id"
            if int(form.customer_SSH_id.data)>0:
                id=form.customer_SSH_id.data
                filter_by="customer_SSH_id"
            if not id and filter_by=="":
                flash('Please give atleast one feild so that can search customer','danger')
            else:
                return redirect(url_for('single_customer',id=id,filter_by=filter_by))
        return render_template('customer/searchcustomer.html',form=form,title="Search customer")
    except Exception as e:
        flash('Internal server error','danger')
        return redirect(url_for('index'))