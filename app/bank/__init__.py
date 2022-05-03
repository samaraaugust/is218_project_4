from flask import Blueprint, render_template, abort, current_app, url_for
from flask_login import login_required, current_user
from app.bank.forms import csv_upload
from jinja2 import TemplateNotFound
from werkzeug.utils import secure_filename, redirect
import os
import csv
from app.db.models import Bank, User
from app.db import db
import logging

bank = Blueprint('bank', __name__,
                        template_folder='templates')

@bank.route('/bank_datatables', methods=['GET'])
@login_required
def browse_bank_datatables():
    log3 = logging.getLogger("request")
    log3.info("Request Method: browse_bank_datatables")
    idNum = User.get_id(current_user)
    data = Bank.query.filter_by(user_id=idNum)
    data_deb = Bank.query.filter_by(user_id=idNum, type='DEBIT')
    data_cred = Bank.query.filter_by(user_id=idNum, type='CREDIT')
    #print(data)
    balance_debit = 0
    for i in data_deb:
        balance_debit = balance_debit + float(i.amount)
    #print(balance_debit)
    balance_credit = 0
    for p in data_cred:
        balance_credit = balance_credit + float(p.amount)
    final_val = 0
    final_val = str(balance_credit + balance_debit)
    value = Bank.query.filter_by(user_id=idNum).count()
    print(value)
    try:
        return render_template('browse_bank_datatables.html',data=data, final_val=final_val, value=value)
    except TemplateNotFound:
        abort(404)


@bank.route('/bank/upload', methods=['POST', 'GET'])
@login_required
def bank_upload():
    log3 = logging.getLogger("request")
    log3.info("Request Method: bank_upload")
    form = csv_upload()
    if form.validate_on_submit():
        log = logging.getLogger("myApp")
        log2 = logging.getLogger("csv")
        filename = secure_filename(form.file.data.filename)
        log2.info("CSV Uploaded: " + filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        form.file.data.save(filepath)
        list_of_transactions = []
        with open(filepath, encoding='utf-8-sig') as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                list_of_transactions.append(Bank(row['AMOUNT'], row['TYPE']))
        current_user.bank = list_of_transactions + current_user.bank
        db.session.commit()
        return redirect(url_for('bank.browse_bank_datatables'))
    try:
        return render_template('upload.html', form=form)
    except TemplateNotFound:
        abort(404)