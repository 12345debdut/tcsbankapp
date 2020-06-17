from flask import flash,redirect,render_template,url_for,request
from bank import db
from bank.forms import CustomerAccountCreateForm,AccountSearch
from bank.models import Customer,CustomerAccount,TransactionInfo
def create_account_view():
    try:
        customer_id=request.args.get('customer_id',"")
        form=CustomerAccountCreateForm()
        if form.validate_on_submit():
            id=form.customer_id.data
            customer=Customer.query.filter_by(customer_id=id).first()
            if customer:
                account_type="savings"
                if str(form.account_type.data)=='1':
                    account_type="savings"
                if str(form.account_type.data)=='2':
                    account_type="current"
                caccount=CustomerAccount(customer_id=form.customer_id.data,account_type=account_type,deposit_amount=form.deposit_amount.data)
                db.session.add(caccount)
                db.session.commit()
                flash(f'Successfully created account for Customer id: {form.customer_id.data}','success')
            else:
                flash(f'Please provide valid customer_id','danger')
        return render_template('account/createaccount.html',form=form,customer_id=customer_id,title="Create account")
    except Exception as e:
        print(e)
        flash('Internal server error','danger')
        return redirect(url_for('index'))

def account_status_view():
    try:
        page=request.args.get('page',1,type=int)
        customeraccount=CustomerAccount.query.paginate(page=page,per_page=10)
        return render_template('account/allaccount.html',customeraccounts=customeraccount,page=page,title="Account status")
    except Exception as e:
        flash('Internal server error','danger')
        return redirect(url_for('index'))

def delete_account_view():
    try:
        account_id=request.args.get('account_id',None)
        conf_delete=request.args.get('conf_delete',False)
        if account_id:
            account=CustomerAccount.query.filter_by(account_id=account_id).first()
            TransactionInfo.query.filter_by(account_id=account_id).delete()
            if account and conf_delete:
                db.session.delete(account)
                db.session.commit()
                flash(f'Successfully deleted the account account id: {account_id}','success')
                return redirect(url_for('account_status'))
        else:
            flash(f'Please provide valid account_id','danger')
        return render_template('account/deleteaccount.html',account=account,title="Delete account")
    except Exception as e:
        print(e)
        flash('Internal server error','danger')
        return redirect(url_for('index'))

def single_account_view():
    try:
        account=None
        try:
            id=int(request.args.get('id'))
            filter_by=request.args.get('filter_by')
        except:
            return redirect(url_for('index'))
        if filter_by=="customer_id":
            account=CustomerAccount.query.filter_by(customer_id=id).first()
        elif filter_by=="account_id":
            account=CustomerAccount.query.filter_by(account_id=id).first()
        else:
            return redirect(url_for('index'))
        
        return render_template('account/singleaccount.html',account=account,title="Account details")
    except Exception as e:
        flash('Internal server error','danger')
        return redirect(url_for('index'))

def account_search_view():
    try:
        form=AccountSearch()
        id=None
        filter_by=""
        if form.validate_on_submit():
            if int(form.account_id.data)>0:
                id=form.account_id.data
                filter_by="account_id"
            if int(form.customer_id.data)>0:
                id=form.customer_id.data
                filter_by="customer_id"
            if not id and filter_by=="":
                flash('Please provide valid information')
            else:
                return redirect(url_for('single_account',id=id,filter_by=filter_by))
        return render_template('account/accountsearch.html',form=form,title="Account search")
    except Exception as e:
        flash('Internal server error','danger')
        return redirect(url_for('index'))


