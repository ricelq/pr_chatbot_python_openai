# This file is part of the Prodeimat project
# @Author: Ricel Quispe

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from ..models import User, Article
from ..database import db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
     
    if request.method == 'POST':
    
        # get the username and password from the form
        username = request.form.get('username')
        password = request.form.get('password')

        # check if user already exists
        exists = db.session.query(User.username).filter_by(username=username).first() 
        if exists:
            flash('Username already exists.', 'danger')
            return redirect(url_for('auth.register'))

        # create new user with hashed password
        new_user = User(username=username, password=generate_password_hash(password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()

        # automatically log in the user after registering
        login_user(new_user)
        return redirect(url_for('main.chat'))

    return render_template('auth/register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.chat'))
      
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        user = db.session.query(User).filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.chat'))
        flash('Invalid username or password', 'danger')


    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))