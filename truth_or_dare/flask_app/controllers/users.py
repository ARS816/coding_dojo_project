from flask import render_template, request, redirect, flash, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/login_and_registration')
def log_reg():
    return render_template('login.html')

@app.route('/login', methods = ['POST'])
def user_login():
    user = User.get_by_email(request.form)
    if not user:
        flash('Invalid Email', 'login')
        return redirect('/login_and_registration')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid Password', 'login')
        return redirect('/login_and_registration')
    session ['id']= user.id
    return redirect('/profile')


@app.route('/register', methods = ['POST'])
def register_user():
    if not User.validate_user(request.form):
        return redirect('/login_and_registration')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'username': request.form['username'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['id'] = id
    return redirect('/profile')

@app.route('/profile')
def profile():
    data = {'id': session['id']}
    return render_template('profile.html', user = User.get_one(data), posts = Post.get_all(), challenge = Post.get_description())


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

