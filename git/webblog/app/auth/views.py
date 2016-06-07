from flask import render_template,redirect,request,url_for,flash
from . import auth
from flask.ext.login import login_user,logout_user,login_required
from ..models import User
from .forms import LoginForm,RegistrationForm
from app import db

@auth.route('/login',methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('错误的用户名或者密码')
    return render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已退出')
    return redirect(url_for('.login'))

@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('你可以登录了')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)

