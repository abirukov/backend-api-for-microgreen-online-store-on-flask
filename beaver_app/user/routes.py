from datetime import datetime

from flask import Blueprint, flash, render_template, redirect, url_for
from beaver_app import db

blueprint = Blueprint('user', __name__, url_prefix='/user')


@blueprint.route('/login')
def login():
    pass
    # if current_user.is_authenticated:
    #     return redirect(get_redirect_target())
    # title = "Авторизация"
    # login_form = LoginForm()
    # return render_template('user/login.html', page_title=title, form=login_form)


@blueprint.route('/logout')
def logout():
    pass


@blueprint.route('/register')
def register():
    pass


@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    pass
