from flask import Blueprint, render_template, abort, current_app, url_for
from flask_login import login_required, current_user
from app.bank.forms import csv_upload
from jinja2 import TemplateNotFound
from werkzeug.utils import secure_filename, redirect
import os
import csv
from app.db.models import Bank
from app.db import db

bank = Blueprint('bank', __name__,
                        template_folder='templates')

@bank.route('/bank', methods=['GET'], defaults={"page": 1})
@bank.route('/bank/<int:page>', methods=['GET'])
def bank_browse(page):
    page = page
    per_page = 1000
    pagination = Bank.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    try:
        return render_template('browse_transactions.html',data=data,pagination=pagination)
    except TemplateNotFound:
        abort(404)

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