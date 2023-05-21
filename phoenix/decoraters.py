from flask import Blueprint, redirect, render_template, session, request, flash, url_for
from flask_login import current_user
from functools import wraps
from .registration.models import Account


def logout_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash("You are already authenticated.", "info")
            return redirect(url_for("main.index"))
        return func(*args, **kwargs)

    return decorated_function


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("You are not authenticated.", "info")
            return redirect(url_for("auth.auth"))
        return func(*args, **kwargs)

    return decorated_function


def manager_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        account = Account.query.filter_by(account_id=current_user.get_id()).first()

        if not account.account_manager_id:
            flash("You are manager, great.", "info")
            return redirect(url_for("main.index"))
        return func(*args, **kwargs)

    return decorated_function


def trainer_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        account = Account.query.filter_by(account_id=current_user.get_id()).first()

        if not account.account_trainer_id:
            flash("You are trainer, great.", "info")
            return redirect(url_for("main.index"))
        return func(*args, **kwargs)

    return decorated_function
