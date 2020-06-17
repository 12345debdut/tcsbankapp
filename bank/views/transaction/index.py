from flask import flash,redirect,render_template,url_for,request
from bank import db
from bank.models import TransactionInfo
from bank.forms import FilterTransaction
def all_transaction_view():
    try:
        page=request.args.get('page',1,type=int)
        tran_type=request.args.get('tran_type',None)
        transfer=False
        all=False
        if tran_type=="all":
            transfers=TransactionInfo.query.order_by(TransactionInfo.action_date.desc()).paginate(page=page,per_page=10)
            all=True
        elif tran_type=="deposit":
            transfers=TransactionInfo.query.filter_by(deposit=1).order_by(TransactionInfo.action_date.desc()).paginate(page=page,per_page=10)
        elif tran_type=="withdraw":
            transfers=TransactionInfo.query.filter_by(deposit=0,transfer=0).order_by(TransactionInfo.action_date.desc()).paginate(page=page,per_page=10)
        elif tran_type=="transfer":
            transfers=TransactionInfo.query.filter_by(transfer=1).order_by(TransactionInfo.action_date.desc()).paginate(page=page,per_page=10)
            transfer=True
        else:
            flash("Please give valid option!!",'danger')
            return redirect('index')
        return render_template('transaction/transactionlist.html',transfers=transfers,all=all,transfer=transfer,title="Transaction list")
    except Exception as e:
        flash('Internal server error','danger')
        return redirect(url_for('index'))

def filter_transaction_view():
    try:
        form=FilterTransaction()
        transaction=None
        account_id=None
        start_date=None
        end_date=None
        if form.validate_on_submit():
            account_id=form.account_id.data
            start_date=form.start_date.data
            end_date=form.end_date.data
            transaction=TransactionInfo.query.filter_by(account_id=account_id).filter(db.func.date(TransactionInfo.action_date)<=end_date,db.func.date(TransactionInfo.action_date)>=start_date).order_by(TransactionInfo.action_date.desc()).all()       
        return render_template('transaction/filter.html',form=form,transactions=transaction,title="Filter transaction",start_date=start_date,end_date=end_date,account_id=account_id)
    except Exception as e:
        print(e)
        flash('Internal server error','danger')
        return redirect(url_for('index'))