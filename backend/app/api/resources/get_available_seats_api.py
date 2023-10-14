from flask import make_response
from app.utils.db import get_db_connection_guest_user
from flask_restful import Resource, abort
from app.utils.validators import validate_flight_id


class GetAvailableSeats(Resource):
    def get(self, flight_id):
        try:
            connection = get_db_connection_guest_user()
        except Exception as ex:
            return abort(500, message=f"Failed to connect to database. Error: {ex}")

        if connection:
            try:
                cursor = connection.cursor()

                # Validate flight ID
                if not validate_flight_id(flight_id):
                    raise Exception("Invalid flight ID")

                # Get all reserved seats for a flight
                cursor.execute(f"SELECT * FROM seat_reservation WHERE ID = {int(flight_id)}")
                query_result = cursor.fetchall()

                response = {}

                # Check if flight exists
                if query_result == []:
                    raise Exception("404")

                # Get available seats for each class
                for item in query_result:
                    className, totalCount, reservedCount, bookedSeats = item[1], item[2], item[3], item[4]
                    availableCount = totalCount - reservedCount
                    if availableCount > 0:
                        availableSeats = set(range(1, totalCount + 1)) - set(int(num) for num in bookedSeats.split(',') if num != '')
                        response[className] = sorted(list(availableSeats))
                    else:
                        response[className] = []

                connection.close()
                return make_response(response, 200)
            except Exception as ex:
                if str(ex) == "404":
                    return abort(404, message=f"Flight with ID {flight_id} does not exist")
                print(ex)
                return abort(400, message=f"Failed to get available seats. Error: {ex}.")
        else:
            return abort(403, message="Unauthorized Access")
