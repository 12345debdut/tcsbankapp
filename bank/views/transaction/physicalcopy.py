from flask import flash,redirect,render_template,url_for,request,make_response
import flask_excel as excel
import pdfkit
import os
from bank import db,app
from bank.models import TransactionInfo
from decouple import config
excel.init_excel(app)
path_wkthmltopdf = os.environ.get('PDF_WKTHTMLTOPDF_PATH') or os.path.join(os.getcwd(),'bank','wkhtmltopdf','bin','wkhtmltopdf.exe') 
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

def generate_pdf_view(start_date,end_date):
    try:
        account_id=request.args.get('account_id',None)
        if account_id and start_date and end_date:
            transaction=TransactionInfo.query.filter(db.func.date(TransactionInfo.action_date)<=end_date,db.func.date(TransactionInfo.action_date)>=start_date).order_by(TransactionInfo.action_date.desc()).all()       
            string=render_template('transaction/pdf.html',transactions=transaction,title='Transaction PDF File')
            pdf=pdfkit.from_string(string,False,configuration=config)
            response=make_response(pdf)
            response.headers['Content-Type']='application/pdf'
            response.headers['Content-Disposition']=f'inline;filename=transaction_{transaction[0].account_id}_{start_date}_{end_date}.pdf'
            return response
        else:
            print(account_id,start_date,end_date)
            return redirect(url_for('index'))
    except Exception as e:
        print(e)
        flash('Please use windows to generate pdf or else download wkhtmltopdf from their download page for the server','danger')
        return redirect(url_for('index'))

def generate_excel_view(start_date,end_date):
    try:
        account_id=request.args.get('account_id',None)
        if account_id and start_date and end_date:
            transactions=TransactionInfo.query.filter(db.func.date(TransactionInfo.action_date)<=end_date,db.func.date(TransactionInfo.action_date)>=start_date).order_by(TransactionInfo.action_date.desc()).all()       
            lst=[["Transaction id","Account id","Amount","Action","Transfer account id"]]
            for transaction in transactions:
                action=""
                transfer_id="Nothing"
                if transaction.deposit==1:
                    action="deposit"
                elif transaction.deposit==0 and transaction.transfer==0:
                    action="withdraw"
                elif transaction.transfer==1:
                    transfer_id=transaction.transfer_account_id
                    action="transfer"
                else:
                    action="unknown"
                lst.append([transaction.transaction_id,transaction.account_id,transaction.amount,action,transfer_id])
            return excel.make_response_from_array(lst, "csv",file_name=f'transaction_{transactions[0].account_id}_{start_date}_{end_date}')
        else:
            print(account_id,start_date,end_date)
            return redirect(url_for('index'))
    except Exception as e:
        print(e)
        flash('Internal server error')
        return redirect(url_for('index'))