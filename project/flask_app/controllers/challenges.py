from flask import render_template, request, redirect, flash, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.challenge import Challenge


@app.route('/challenge/new')
def new():
    data = {'id': session['id']}
    return render_template('create.html', user = User.get_one(data))

@app.route('/challenges/new/add', methods=['POST'])
def add_challenge():
    if not Challenge.validate_challenge(request.form):
        return redirect ('/challenge/new')
    Challenge.save(request.form)
    return redirect('/challenges/all')

@app.route('/challenges/all')
def all_challenges():
    data = {'id': session['id']}
    return render_template('all_challenges.html', user = User.get_one(data), challenges = Challenge.get_all())

@app.route('/challenges/edit/<int:id>')
def edit_challenge(id):
    challenge = Challenge.get_by_id(id)
    data = {'id': session['id']}
    user = User.get_one(data)
    return render_template('edit.html', challenge = challenge, user = user)

@app.route("/challenges/edit/update", methods = ["POST"])
def update():
    if not Challenge.validate_challenge(request.form):
        return redirect(f"/challenges/edit/{request.form['id']}")
    Challenge.update(request.form)
    return redirect('/challenges/all')

@app.route('/challenges/delete/<int:id>')
def delete_post(id):
    Challenge.delete(id)
    return redirect('/challenges/all')