from flask import Blueprint, render_template, abort, current_app, url_for
from flask_login import login_required, current_user
from app.bank.forms import csv_upload
from jinja2 import TemplateNotFound
from werkzeug.utils import secure_filename, redirect
import os
import csv
from app.db.models import Bank
from app.db import db
from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
bank = Blueprint('bank', __name__,
                        template_folder='templates')

@bank.route('/bank', methods=['GET'], defaults={"page": 1})
@bank.route('/bank/<int:page>', methods=['GET'])
@login_required
def bank_browse(page):
    engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
    Session = sessionmaker(bind=engine)
    session = Session()
    page = page
    per_page = 1000
    pagination = Bank.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    balance_debit = 0
    data_sec = session.query(Bank).filter(Bank.type=='DEBIT').all()
    for i in data_sec:
        print(i.amount)
        balance_debit = balance_debit + float(i.amount)
    print("D: ", balance_debit)
    data_cred = session.query(Bank).filter(Bank.type=='CREDIT').all()
    balance_credit = 0
    for p in data_cred:
        print(p.amount)
        balance_credit = balance_credit + float(p.amount)
    print("finalC: ", balance_credit)
    final_val = str(balance_credit + balance_debit)
    print("final Val: ", final_val)
    #data_sec = Bank.query.all()

    try:
        return render_template('browse_transactions.html',data=data,pagination=pagination, data_sec=data_sec, data_cred=data_cred, final_val=final_val)
    except TemplateNotFound:
        abort(404)

@bank.route('/bank/account', methods=['GET'])
def account_balence():
    balence = 0
    data = Bank.query.all()
    print(data)



@bank.route('/bank/upload', methods=['POST', 'GET'])
@login_required
def bank_upload():
    form = csv_upload()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        form.file.data.save(filepath)
        list_of_transactions = []
        with open(filepath, encoding='utf-8-sig') as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                list_of_transactions.append(Bank(row['AMOUNT'], row['TYPE']))
        current_user.bank = list_of_transactions
        db.session.commit()
        return redirect(url_for('bank.bank_browse'))
    try:
        return render_template('upload.html', form=form)
    except TemplateNotFound:
        abort(404)