from flask_app.config.mysqlconnection import connectToMySQL 
from flask import flash
from flask_app.models.user import User

class Challenge:
    def __init__(self,data):
        self.id = data['id']
        self.description= data['description']
        self.type= data['type']
        self.created_at= data['created_at']
        self.updated_at= data['updated_at']
        self.user_id = data['user_id']


    @classmethod
    def save(cls, data):
        query = "INSERT INTO challenges (description, type, user_id) VALUES( %(description)s, %(type)s, %(user_id)s);"
        return connectToMySQL('challenge_schema').query_db(query,data)

    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * from challenges JOIN users on challenges.user_id = users.id WHERE challenges.id = %(id)s"
        results = connectToMySQL('challenge_schema').query_db(query, {"id": id})
        print(results[0])
        show_challenge = results[0]
        challenge = Challenge(show_challenge)
        user =  User({
                "id": show_challenge["user_id"],
                "email": show_challenge["email"],
                "first_name": show_challenge["first_name"],
                "last_name":show_challenge["last_name"],
                "password": show_challenge["password"]
            })
        challenge.user = user
        return challenge

    @classmethod
    def get_all(cls):
        query = """SELECT * from challenges
                    JOIN users on challenges.user_id = users.id;"""
        results = connectToMySQL('challenge_schema').query_db(query)
        all_challenges = []
        for row in results:
            posting_user = User({
                "id": row["user_id"],
                "email": row["email"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "username": row["username"],
                "password": row["password"]
            })
            new_challenge = Challenge({
                "id": row["id"],
                "description": row["description"],
                "type": row["type"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "user_id": posting_user
            })
            all_challenges.append(new_challenge)
        return all_challenges

    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * from challenges JOIN users on challenges.user_id = users.id WHERE challenges.id = %(id)s"
        results = connectToMySQL('challenge_schema').query_db(query, {"id": id})
        print(results[0])
        show_challenge = results[0]
        challenge = Challenge(show_challenge)
        user =  User({
                "id": show_challenge["user_id"],
                "email": show_challenge["email"],
                "first_name": show_challenge["first_name"],
                "last_name":show_challenge["last_name"],
                "password": show_challenge["password"],
                "username": show_challenge["username"]
            })
        challenge.user = user
        return challenge
    
    @classmethod
    def update(cls,data):
        query= "UPDATE challenges SET description = %(description)s, type = %(type)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('challenge_schema').query_db(query,data)
    
    @classmethod
    def delete(cls, id):
            query = "DELETE from challenges WHERE challenges.id = %(id)s;"
            connectToMySQL('challenge_schema').query_db(query, {"id": id})
            return id
    
    @staticmethod
    def validate_challenge(data):
        is_valid = True
        if len(data["description"]) < 3:
            flash("Please enter a description", "challenges")
            is_valid = False
        if "type" not in data:
            flash("Challenge type required.", "challenges")
            is_valid = False
        return is_valid