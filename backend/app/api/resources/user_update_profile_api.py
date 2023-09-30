from flask import jsonify, make_response
from app.utils.db import get_db_connection
from flask_restful import Resource, abort, reqparse
from app.utils.validators import validate_user_update_data_with_password, validate_user_update_data_without_password, validate_Username
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

parser = reqparse.RequestParser()
parser.add_argument('firstname', type=str, required=True)
parser.add_argument('lastname', type=str, required=True)
parser.add_argument('currentPassword', type=str, required=False)
parser.add_argument('newPassword', type=str, required=False)


class UpdateUser(Resource):
    @jwt_required()
    def patch(self):
        try:
            connection = get_db_connection()
        except Exception as ex:
            return abort(500, message=f"Failed to connect to database. Error: {ex}")
        
        if connection:
            try:
                cursor = connection.cursor()

                try:
                    args = parser.parse_args()
                except Exception:
                    raise Exception("Incomplete user data or invalid JSON object")
                
                firstname = args['firstname']
                lastname = args['lastname']
                current_password = args['currentPassword']
                new_password = args['newPassword']
                
                # Get current user
                current_user = get_jwt_identity()

                if current_password is None or new_password is None:
                    # Validate user data
                    if not validate_user_update_data_without_password(firstname, lastname):
                        raise Exception("Invalid user data")
                    
                    # update user
                    cursor.execute(f"UPDATE user SET FirstName = '{firstname}', LastName = '{lastname}' WHERE Username = '{current_user}'")

                else:
                    # Validate user data
                    if not validate_user_update_data_with_password(firstname, lastname, current_password, new_password):
                        raise Exception("Invalid user data")
                    
                    # Check if current password is correct
                    cursor.execute(f"SELECT Password FROM user WHERE Username = '{current_user}'")
                    passwordfetched = cursor.fetchone()
                    if passwordfetched is None:
                        raise Exception("Invalid username")
                    if not check_password_hash(passwordfetched[0], current_password):
                        raise Exception("Incorrect password")
                    
                    # update user
                    hashed_password = generate_password_hash(new_password.strip(), method='scrypt')
                    cursor.execute(f"UPDATE user SET FirstName = '{firstname}', LastName = '{lastname}', Password = '{hashed_password}' WHERE Username = '{current_user}'")
                
                connection.commit()
                connection.close()

                return make_response({"message": "User updated successfully"}, 200)
            
            except Exception as ex:
                return abort(400, message=f"Failed to update user. Error: {ex}.")
        else:
            return abort(500, message="Failed to connect to database")
        
