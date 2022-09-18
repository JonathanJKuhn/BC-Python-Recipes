from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

class Recipe:
    def __init__(self, db_data) -> None:
        self.id = db_data['id']
        self.name = db_data['name']
        self.description = db_data['description']
        self.instructions = db_data['instructions']
        self.date_made = db_data['date_made']
        self.under_30 = bool(db_data['under_30'])
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.user = None

    @staticmethod
    def add(data):
        query = "INSERT INTO recipes (name,description,instructions,date_made,under_30,user_id) VALUES (%(name)s,%(description)s,%(instructions)s,%(date_made)s,%(under_30)s,%(user_id)s);"
        result = connectToMySQL('recipes_schema').query_db(query, data)
        return result

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON user_id = users.id"
        result = connectToMySQL('recipes_schema').query_db(query)
        
        recipe_list = []
        for item in result:
            user_data = {
                'id': item['users.id'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                'email': item['email'],
                'password': item['password'],
                'created_at': item['users.created_at'],
                'updated_at': item['users.updated_at']
            }
            user_obj = User(user_data)

            recipe_data = {
                'id': item['id'],
                'name': item['name'],
                'description': item['description'],
                'instructions': item['instructions'],
                'date_made': item['date_made'],
                'under_30': item['under_30'],
                'created_at': item['created_at'],
                'updated_at': item['updated_at'],
                'user_id': item['user_id'],
            }
            recipe_obj = cls(recipe_data)
            recipe_obj.user = user_obj
            recipe_list.append(recipe_obj)

        return recipe_list

    @classmethod
    def get_one_by_id(cls, data):
        query = "Select * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL('recipes_schema').query_db(query,data)
        return cls(result[0])

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("Name isn't long enough - Min 3")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description isn't long enough - Min 3")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Instructions aren't long enough - Min 3")
            is_valid = False
        if len(recipe['name']) < 3:
            flash("Name isn't long enough - Min 3")
            is_valid = False
        if not recipe['date_made']:
            flash("Please select a Date Cooked/Made")
            is_valid = False
        return is_valid