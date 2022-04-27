from flask import Blueprint, render_template, abort
from flask_login import login_required
from app.bank.forms import csv_upload
from jinja2 import TemplateNotFound
bank = Blueprint('bank', __name__,
                        template_folder='templates')

@bank.route('/bank/upload', methods=['POST', 'GET'])
@login_required
def bank_upload():
    form = csv_upload()
    
    try:
        return render_template('upload.html', form=form)
    except TemplateNotFound:
        abort(404)