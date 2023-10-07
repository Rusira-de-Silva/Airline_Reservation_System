from flask import jsonify
from app.utils.db import get_db_connection
from flask_restful import Resource, abort, reqparse
from app.utils.validators import validate_user_data
from werkzeug.security import check_password_hash
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True)
parser.add_argument('password', type=str, required=True)


class GetAuthToken(Resource):
    def post(self):
        try:
            connection = get_db_connection()
        except Exception as ex:
            return abort(500, message=f"Failed to connect to database. Error: {ex}")
        
        if connection:
            try:
                cursor = connection.cursor()
                args = parser.parse_args()
                username = args['username']
                password = args['password']
                # SQL query to get user
                query = "SELECT Username, Password FROM User where Username = %s"
                # Execute query with username
                cursor.execute(query,(username,))    # parameter values must be in a tuple
                items = cursor.fetchone()
                connection.close()
                if items is None:
                    return jsonify({'message': 'Invalid username or password'})
                else:
                    if check_password_hash(items[1], password):
                        access_token = create_access_token(identity=username)
                        return jsonify({'message': 'Login successful', 'access_token': access_token})
                    else:
                        return jsonify({'message': 'Invalid username or password'})
            except Exception as ex:
                print(ex)
                return abort(400, message=f"Failed to get user. Error: {ex}")
        else:
            return abort(500, message="Failed to connect to database")


class GetUserDetails(Resource):
    @jwt_required()     # check if user is jwt authenticated
    def get(self):
        try:
            connection = get_db_connection()
        except Exception as ex:
            return abort(500, message=f"Failed to connect to database. Error: {ex}")
        
        if connection:
            try:
                cursor = connection.cursor()
                username = get_jwt_identity()
                # SQL query to get user details
                query = """
                SELECT Username, FirstName, LastName, Category_Name
                FROM User join Category on User.Category = Category.Category_ID
                where Username = %s
                """
                # Execute query with username
                cursor.execute(query,(username,))
                items = cursor.fetchone()
                response = {
                    'username': items[0],
                    'firstName': items[1],
                    'lastName': items[2],
                    'category': items[3]
                }
                connection.close()
                if items is None:
                    return abort(500, message="No User Found with credentials")
                else:
                    return jsonify(response)
            except Exception as ex:
                print(ex)
                return abort(400, message=f"Failed to Access URL. Error: {ex}")
        else:
            return abort(500, message="Failed to connect to database")

