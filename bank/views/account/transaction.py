from flask import flash,redirect,render_template,url_for,request
from bank import db
from bank.models import CustomerAccount,TransactionInfo
from bank.forms import DepositAmount,WithDrawAmount,TransferAmount
from bank.decorator import customer_activation_required
import uuid
@customer_activation_required
def deposit_account_view():
    try:
        form=DepositAmount()
        try:
            account_id=int(request.args.get('account_id'))
        except:
            return redirect(url_for('index'))
        if account_id:
            account=CustomerAccount.query.filter_by(account_id=account_id).first()
        if form.validate_on_submit() and account:
            amount=form.amount.data
            finalamount=amount+account.deposit_amount
            account.deposit_amount=finalamount
            db.session.commit()
            id=uuid.uuid1()
            transaction=TransactionInfo(account_id=account_id,amount=amount,transaction_id=id.hex,deposit=True,transfer=False,transfer_account_id=0)
            db.session.add(transaction)
            db.session.commit()
            flash(f'Successfully credited the amount: {amount} and final balance is: {finalamount}','success')
            return redirect(url_for('account_search'))
        return render_template('account/depositaccount.html',account=account,form=form,title="Deposit cash")
    except Exception as e:
        flash('Internal server error','danger')
        return redirect(url_for('index'))

@customer_activation_required
def withdraw_account_view():
    try:
        form=WithDrawAmount()
        try:
            account_id=int(request.args.get('account_id'))
        except:
            return redirect(url_for('index'))
        if account_id:
            account=CustomerAccount.query.filter_by(account_id=account_id).first()
        if form.validate_on_submit() and account:
            amount=form.amount.data
            finalamount=account.deposit_amount-amount
            account.deposit_amount=finalamount
            db.session.commit()
            id=uuid.uuid1()
            transaction=TransactionInfo(account_id=account_id,amount=amount,transaction_id=id.hex,deposit=False,transfer=False,transfer_account_id=0)
            db.session.add(transaction)
            db.session.commit()
            flash(f'Successfully debited the amount: {amount} and final balance is: {finalamount}','success')
            return redirect(url_for('account_search'))
        return render_template('account/withdrawaccount.html',account=account,form=form,title="Withdraw cash")
    except Exception as e:
        print(e)
        flash('Internal server error','danger')
        return redirect(url_for('index'))

@customer_activation_required
def transfer_account_view():
    try:
        form=TransferAmount()
        try:
            account_id=int(request.args.get('account_id'))
        except:
            return redirect(url_for('index'))
        if account_id:
            account=CustomerAccount.query.filter_by(account_id=account_id).first()
        if form.validate_on_submit() and account:
            amount=form.amount.data
            transfer_account_id=form.transfer_account.data
            transfer=CustomerAccount.query.filter_by(account_id=transfer_account_id).first()
            if not transfer:
                flash(f"Please provide valid transfer id {transfer_account_id}",'danger')
                return redirect(url_for('index'))
            if account.account_id==transfer.account_id:
                flash("You have added from and to account same!!",'danger')
                return redirect(url_for('account_search'))
            if account.deposit_amount-amount<0:
                flash(f'Not enough balance to transact!!!')
                return redirect(url_for('account_search'))
            finalamount=account.deposit_amount-amount
            account.deposit_amount=finalamount
            db.session.commit()
            finalamount=transfer.deposit_amount+amount
            transfer.deposit_amount=finalamount
            db.session.commit()
            id=uuid.uuid1()
            transaction=TransactionInfo(account_id=account_id,amount=amount,transaction_id=id.hex,deposit=False,transfer=True,transfer_account_id=transfer_account_id)
            db.session.add(transaction)
            db.session.commit()
            flash(f'{amount} is transfered from {account.account_id} to {transfer_account_id}','success')
            return redirect(url_for('account_search'))
        return render_template('account/transferaccount.html',account=account,form=form,title="Transfer cash")
    except Exception as e:
        print(e)
        flash('Internal server error','danger')
        return redirect(url_for('index'))