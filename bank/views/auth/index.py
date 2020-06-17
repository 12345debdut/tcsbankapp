from flask import flash,redirect,render_template,url_for
from flask_login import login_user,logout_user
from bank import db,bcrypt
from bank.forms import LoginForm
from bank.models import User

def login_view():
    try:
        form=LoginForm()
        if form.validate_on_submit():
            user=User.query.filter_by(username=form.username.data).first()
            if user and bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user,remember=True)
                flash(f'You have successfully logged in {user.username}','success')
                return redirect(url_for('index'))
            else:
                flash('Please check your username or password','danger')
        return render_template('auth/login.html',title="Log in",form=form)
    except Exception as e:
        print(e)
        flash('Internal server error','danger')
        return redirect(url_for('index'))

def logout_view():
    try:
        logout_user()
        flash('User successfully logged out','success')
        return redirect('/')
    except Exception as e:
        print(e)
        flash('Internal server error','danger')
        return redirect(url_for('index'))