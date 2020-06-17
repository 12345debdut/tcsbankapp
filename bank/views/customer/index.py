from flask import flash,redirect,render_template,url_for,request,abort,jsonify
from bank import db
from bank.models import Customer,CustomerAccount
from bank.api_schema import customer_schema
from bank.forms import CustomerCreateForm,CustomerUpdateForm
from bank.country_state import state
import datetime
def create_customer_view():
    try:
        form=CustomerCreateForm()
        if form.validate_on_submit():
            statetemp="default"
            for item in state:
                if(item[0]==str(form.state.data)):
                    statetemp=item[1]
                    break
            customer=Customer(SSH_id=form.SSH_id.data,name=form.name.data,age=form.age.data,address=form.address.data,state=statetemp,city=form.city.data,active=False,message=f"Customer account successfully created on {datetime.datetime.now()}")
            db.session.add(customer)
            db.session.commit()
            flash(f'Successfully created {form.name.data} customer!!!','success')
            return redirect(url_for('index'))
        return render_template('customer/create.html',form=form,title="Create customer")
    except Exception as e:
        print(e)
        flash('Internal server error','danger')
        return redirect(url_for('index'))

def all_customer_view():
    try:
        page=request.args.get('page',1,type=int)
        customers=Customer.query.paginate(page=page,per_page=10)
        return render_template('customer/allcustomer.html',customers=customers,page=page,title="All Customer")
    except Exception as e:
        print(e)
        flash('Internal server error','danger')
        return redirect(url_for('index'))

def edit_customer_view():
    try:
        customer=Customer.query.filter_by(SSH_id=request.args.get('id')).first()
        form=CustomerUpdateForm()
        statetemp="1"
        for item in state:
            if(item[1]==customer.state):
                statetemp=item[0]
                break
        if form.validate_on_submit():
            statetemp="default"
            for item in state:
                if(item[0]==str(form.state.data)):
                    statetemp=item[1]
                    break
            id=request.args.get('id')
            customer=Customer.query.filter_by(SSH_id=id).first()
            if customer:
                customer.name=form.name.data
                customer.age=form.age.data
                customer.address=form.address.data
                customer.state=statetemp
                customer.city=form.city.data
                customer.active=form.active.data
                customer.message=f"Customer updated successfully on {datetime.datetime.now()}"
                db.session.commit()
                flash(f'Successfully updated the information of {form.name.data}','success')
                return redirect(url_for('all_customer'))
            else:
                flash(f'Please provide a valid information','danger')
        return render_template('customer/editcustomer.html',form=form,customer=customer,state=statetemp,title="Edit customer")
    except Exception as e:
        flash('Internal server error','danger')
        return redirect(url_for('index'))

def delete_customer_view():
    try: 
        id=request.args.get('id')
        conf_delete=request.args.get('conf_delete',False)
        customer=Customer.query.filter_by(SSH_id=id).first()
        if conf_delete:
            CustomerAccount.query.filter_by(customer_id=customer.customer_id).delete()
            db.session.delete(customer)
            db.session.commit()
            flash(f'Successfully deleted the customer','success') 
            return redirect(url_for('all_customer'))        
        return render_template('customer/deletecustomer.html',customer=customer,title="Delete customer")
    except Exception as e:
        print(e)
        flash('Please delete the account of the customer associated with it','danger')
        return redirect(url_for('index'))

def customer_details_view():
    try:
        id=request.args.get('id',None)
        if not id:
            flash(f'Give a valid id','danger')
            return redirect(ur_for('index'))
        customer=Customer.query.filter_by(customer_id=id).first()
        account=CustomerAccount.query.filter_by(customer_id=id).first()
        return render_template('customer/customerdetails.html',customer=customer,account=account)
    except Exception as e:
        print(e)
        flash("Internal server error",'danger')
        return redirect(url_for('index'))

def refresh_api():
    customer_id=request.args.get('customer_id',None)
    if customer_id:
        customer=Customer.query.filter_by(customer_id=customer_id).first()
        jsoncustomer=customer_schema.dump(customer)
        return jsonify(jsoncustomer)
    else:
        return abort(400)