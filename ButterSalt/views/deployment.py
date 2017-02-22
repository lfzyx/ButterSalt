from flask import Blueprint, flash, redirect, url_for
from flask_login import login_required
from flask import render_template
from ButterSalt import app, Token


deployment = Blueprint('deployment', __name__, url_prefix='/deployment')


@deployment.route('/')
@login_required
def index():
    pass
    return render_template('deployment/index.html')