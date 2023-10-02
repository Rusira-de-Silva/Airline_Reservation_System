from flask import make_response
from app.utils.db import get_db_connection
from flask_restful import Resource, abort, reqparse
from app.utils.validators import validate_update_delay_data
from flask_jwt_extended import jwt_required, get_jwt_identity

parser = reqparse.RequestParser()
parser.add_argument('scheduledFlightID', type=int, required=True)
parser.add_argument('delayMinutes', type=int, required=True)


class DEOupdateDelay(Resource):
    @jwt_required()
    def patch(self):
        try:
            connection = get_db_connection()
        except Exception as ex:
            return abort(500, message=f"Failed to connect to the database. Error: {ex}")

        if connection:
            try:
                cursor = connection.cursor()

                try:
                    request_data = parser.parse_args()
                except Exception:
                    raise Exception("Incomplete data or invalid JSON object")
                
                # Retrieve request data
                scheduledFlightID = request_data['scheduledFlightID']
                delayMinutes = request_data['delayMinutes']

                username = get_jwt_identity()
                cursor.execute(f"SELECT IsDataEntryOperator FROM user WHERE Username = '{username}'")
                query_result = cursor.fetchone()

                # Check if user is a data entry operator
                if query_result[0] != 1:  # Check if query_result is None
                    raise Exception("403")
                
                # Validate data
                if not validate_update_delay_data(scheduledFlightID, delayMinutes):
                    raise Exception("Invalid data")
                
                cursor.execute("UPDATE scheduled_flight SET Delay_Minutes = %s WHERE Scheduled_ID = %s", (delayMinutes, scheduledFlightID))

                connection.commit()
                connection.close()
                return make_response("Successfully updated the delay",200)

            except Exception as ex:
                if str(ex) == "403":
                    return abort(403, message="Account is not authorized to perform this action")
                return abort(400, message=f"Failed to update delay. Error: {ex}")
        else:
            return abort(500, message="Failed to connect to the database")