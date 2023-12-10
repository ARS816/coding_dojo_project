from flask import request, redirect, render_template, session
from flask_app import app
from flask_app.models.post import Post
from flask_app.models.user import User
from flask_app.models.challenge import Challenge

@app.route('/new_post', methods=["POST"])
def new_post():
    if not Post.validate_post(request.form):
        return redirect ('/profile')
    Post.save(request.form)
    return redirect('/profile')

@app.route("/delete/<int:id>")
def delete(id):
    Post.delete(id)
    return redirect("/profile")

@app.route("/create_post")
def create_post():
    data = {'id': session['id']}
    return render_template('new_post.html', user = User.get_one(data), challenges = Challenge.get_all())