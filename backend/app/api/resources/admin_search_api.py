from flask import make_response, request
from app.utils.db import get_db_connection
from flask_restful import Resource, abort
from app.utils.validators import validate_origin_destination_parameters, validate_date_range, validate_icao_code
from flask_jwt_extended import jwt_required, get_jwt_identity


class GetPassengersByNextFlight(Resource):
    @jwt_required()
    def get(self):
        try:
            connection = get_db_connection()
        except Exception as ex:
            return abort(500, message=f"Failed to connect to database. Error: {ex}")

        if connection:
            try:
                cursor = connection.cursor()

                # check if user is admin
                username = get_jwt_identity()
                cursor.execute(f"SELECT * FROM staff WHERE Username = '{username}' AND Role = 'Admin'")
                query_result = cursor.fetchone()
                
                if query_result is None or query_result[0] is None:
                    raise Exception("403")
                
                from_airport = request.args.get('fromAirport')
                to_airport = request.args.get('toAirport')

                # Validate search parameters
                if not validate_origin_destination_parameters(from_airport, to_airport):
                    raise Exception("Invalid search parameters")
                
                # Get passengers by flight
                cursor.execute(f"""
                    SELECT 
                        psg.name AS name,
                        psg.seat AS seatNumber,
                        psg.isAdult AS isAdult,
                        psg.flightID AS flightID, 
                        psg.class AS travelClass,
                        psg.isPaymentDone AS isPaymentDone,
                        psg.bookingRefID AS bookingRefID,
                        psg.userType AS userType,
                        psg.passportID AS passportID
                    FROM 
                        passenger as psg
                    WHERE 
                        fromICAO = '{from_airport}' 
                        AND toICAO = '{to_airport}'
                        AND departureDateTime = ( 
                            SELECT MIN(departureDateTime) 
                            FROM passenger 
                            WHERE 
                                fromICAO = '{from_airport}' 
                                AND toICAO = '{to_airport}'
                            AND DATE(departureDateTime) >= CURDATE()
                        );
                """)
                query_result = cursor.fetchall()

                response = []
                for item in query_result:
                    response.append({
                        "name": item[0],
                        "seatNumber": item[1],
                        "isAdult": item[2],
                        "flightID": item[3],
                        "travelClass": item[4],
                        "isPaymentDone": item[5],
                        "bookingRefID": item[6],
                        "userType": item[7],
                        "passportID": item[8]
                    })

                connection.close()
                return make_response(response, 200)
            except Exception as ex:
                if str(ex) == "403":
                    return abort(403, message=f"Account is not an Administarator")
                print(ex)
                return abort(400, message=f"Failed to get passengers by flight. Error: {ex}.")
        else:
            return abort(500, message="Failed to connect to database")


class GetPassengersByDateDestination(Resource):
    @jwt_required()
    def get(self):
        try:
            connection = get_db_connection()
        except Exception as ex:
            return abort(500, message=f"Failed to connect to database. Error: {ex}")

        if connection:
            try:
                cursor = connection.cursor()

                # check if user is admin
                username = get_jwt_identity()
                cursor.execute(f"SELECT * FROM staff WHERE Username = '{username}' AND Role = 'Admin'")
                query_result = cursor.fetchone()
                
                if query_result is None or query_result[0] is None:
                    raise Exception("403")
                
                from_date = request.args.get('fromDate')
                to_date = request.args.get('toDate')
                to_airport = request.args.get('toAirport')

                # Validate search parameters
                if not validate_date_range(from_date, to_date) or not validate_icao_code(to_airport):
                    raise Exception("Invalid search parameters")
                
                # Get passengers by date and destination
                cursor.execute(f"""
                    SELECT COUNT(*) as passengersCount
                    FROM passenger
                    WHERE 
                        DATE(departureDateTime) BETWEEN '{from_date}' AND '{to_date}'
                        AND toICAO = '{to_airport}' ;
                """)
                query_result = cursor.fetchone()

                response = {
                    "passengersCount": query_result[0]
                }

                connection.close()
                return make_response(response, 200)
            except Exception as ex:
                if str(ex) == "403":
                    return abort(403, message=f"Account is not an Administarator")
                print(ex)
                return abort(400, message=f"Failed to get passengers by date and destination. Error: {ex}.")
        else:
            return abort(500, message="Failed to connect to database")
        

class GetBookingCountByDatePassengerType(Resource):
    @jwt_required()
    def get(self):
        try:
            connection = get_db_connection()
        except Exception as ex:
            return abort(500, message=f"Failed to connect to database. Error: {ex}")

        if connection:
            try:
                cursor = connection.cursor()

                # check if user is admin
                username = get_jwt_identity()
                cursor.execute(f"SELECT * FROM staff WHERE Username = '{username}' AND Role = 'Admin'")
                query_result = cursor.fetchone()
                
                if query_result is None or query_result[0] is None:
                    raise Exception("403")
                
                from_date = request.args.get('fromDate')
                to_date = request.args.get('toDate')

                # Validate search parameters
                if not validate_date_range(from_date, to_date):
                    raise Exception("Invalid search parameters")
                
                # Get passengers count by date and passenger types
                cursor.execute(f"""
                    SELECT userType AS passengerType, COUNT(*) as bookingsCount
                    FROM passenger
                    WHERE 
                        DATE(departureDateTime) BETWEEN '{from_date}' AND '{to_date}'
                    GROUP BY userType;
                """)
                query_result = cursor.fetchall()

                response = []
                for item in query_result:
                    response.append({
                        "passengerType": item[0],
                        "bookingsCount": item[1]
                    })

                connection.close()
                return make_response(response, 200)
            except Exception as ex:
                if str(ex) == "403":
                    return abort(403, message=f"Account is not an Administarator")
                print(ex)
                return abort(400, message=f"Failed to get passengers by date and passenger type. Error: {ex}.")
        else:
            return abort(500, message="Failed to connect to database")
        

class GetPastFlightsDetails(Resource):
    @jwt_required()
    def get(self):
        try:
            connection = get_db_connection()
        except Exception as ex:
            return abort(500, message=f"Failed to connect to database. Error: {ex}")

        if connection:
            try:
                cursor = connection.cursor()

                # check if user is admin
                username = get_jwt_identity()
                cursor.execute(f"SELECT * FROM staff WHERE Username = '{username}' AND Role = 'Admin'")
                query_result = cursor.fetchone()
                
                if query_result is None or query_result[0] is None:
                    raise Exception("403")
                
                from_airport = request.args.get('fromAirport')
                to_airport = request.args.get('toAirport')

                # Validate search parameters
                if not validate_origin_destination_parameters(from_airport, to_airport):
                    raise Exception("Invalid search parameters")
                
                # Get flights by origin and destination
                cursor.execute(f"""
                    SELECT
                        shf.Scheduled_ID AS ID,
                        DATE_ADD(shf.Departure_Time, INTERVAL shf.Delay_Minutes MINUTE) AS departureDateAndTime,
                        DATE_ADD(shf.Departure_Time, INTERVAL shf.Delay_Minutes + rut.Duration_Minutes MINUTE) AS arrivalDateAndTime,
                        mdl.Name AS airplaneModel,
                        apl.Tail_Number AS tailNumber,
                        COUNT(Distinct bk.Ticket_Number) AS passengersCount,
                        CASE
                            WHEN shf.Delay_Minutes = 0 THEN 'On Time'
                            ELSE 'Delayed'
                        END AS status
                    FROM
                        booked_seat as bk
                        INNER JOIN booking AS bkset ON bk.booking = bkset.Booking_Ref_ID
                        INNER JOIN scheduled_flight AS shf ON bkset.Scheduled_Flight = shf.Scheduled_ID
                        INNER JOIN route AS rut ON rut.Route_ID = shf.Route
                        INNER JOIN airport AS org ON rut.Origin = org.ICAO_Code
                        INNER JOIN airport AS des ON rut.Destination = des.ICAO_Code
                        INNER JOIN airplane AS apl ON shf.Airplane = apl.Tail_Number
                        INNER JOIN model AS mdl ON apl.Model = mdl.Model_ID
                    WHERE
                        DATE_ADD(shf.Departure_Time, INTERVAL shf.Delay_Minutes + rut.Duration_Minutes MINUTE) < NOW()
                        AND org.ICAO_Code = '{from_airport}' 
                        AND des.ICAO_Code = '{to_airport}'
                    GROUP BY shf.Scheduled_ID;
                """)
                query_result = cursor.fetchall()

                response = []
                for item in query_result:
                    response.append({
                        "ID": item[0],
                        "departureDateAndTime": item[1],
                        "arrivalDateAndTime": item[2],
                        "airplaneModel": item[3],
                        "tailNumber": item[4],
                        "passengersCount": item[5],
                        "status": item[6]
                    })

                connection.close()
                return make_response(response, 200)
            except Exception as ex:
                if str(ex) == "403":
                    return abort(403, message=f"Account is not an Administarator")
                print(ex)
                return abort(400, message=f"Failed to get past flight details. Error: {ex}.")
        else:
            return abort(500, message="Failed to connect to database")

