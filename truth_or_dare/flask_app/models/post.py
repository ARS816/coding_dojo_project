from flask_app.config.mysqlconnection import connectToMySQL 
from flask import flash
from flask_app.models.user import User
from flask_app.models.challenge import Challenge

class Post:
    def __init__(self,data):
        self.id = data['id']
        self.content= data['content']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.challenge_id = data['challenge_id']


    @classmethod
    def save(cls, data):
        query = "INSERT INTO posts (content, user_id, challenge_id) VALUES( %(content)s, %(user_id)s, %(challenge_id)s) ;"
        return connectToMySQL('challenge_schema').query_db(query,data)


    @classmethod
    def get_all(cls):
        query = """SELECT * from posts
                    JOIN users on posts.user_id = users.id;"""
        results = connectToMySQL('challenge_schema').query_db(query)
        all_posts = []
        for row in results:
            posting_user = User({
                "id": row["user_id"],
                "email": row["email"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"],
                "password": row["password"],
                "username": row["username"]
            })
            new_post = Post({
                "id": row["id"],
                "content": row["content"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "user_id": posting_user,
                "challenge_id": row['challenge_id']
            })
            all_posts.append(new_post)
        return all_posts
    
    @classmethod
    def get_description(cls):
        query = """SELECT * from posts
                    JOIN challenges on posts.challenge_id = challenges.id;"""
        results = connectToMySQL('challenge_schema').query_db(query)
        all_posts = []
        for row in results:
            posting_challenge = Challenge({
                "id": row["challenge_id"],
                "description": row["description"],
                "type": row['type'],
                "created_at":row['created_at'],
                "updated_at":row['updated_at'],
                "user_id": row['user_id']
            })
            new_post = Post({
                "id": row["id"],
                "content": row["content"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "user_id": row["user_id"],
                "challenge_id": posting_challenge
            })
            all_posts.append(new_post)
        return all_posts

    @classmethod
    def delete(cls, id):
            query = "DELETE from posts WHERE id = %(id)s;"
            connectToMySQL('challenge_schema').query_db(query, {"id": id})
            return id

    @staticmethod
    def validate_post(data):
            is_valid = True
            if len(data["content"]) == 0:
                flash("Content must not be blank", "posts")
                is_valid = False
            return is_valid
