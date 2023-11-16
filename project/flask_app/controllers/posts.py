from flask import request, redirect
from flask_app import app
from flask_app.models.post import Post



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

