from flask import Flask, request
import os
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)
load_dotenv('.env')


def get_db_connection():
       env = os.environ
       conn = psycopg2.connect(
            database=env.get("DATABASE_NAME"), 
            user=env.get("PG_USERNAME"), 
            password=env.get("PG_PASSWORD"), 
            host=env.get("HOST"), 
            port= env.get("PORT")
       )
       return conn

@app.get('/liveness')
def index():
        return "live"

# query to get all matching offers
def execute_query_matching(departure_airports, earliest_departure_date, latest_return_date, count_adults, count_children, duration, hotelid):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    query = """
        SELECT offer.price, offer.countadults, offer.countchildren, offer.inboundarrivaldatetime, offer.inbounddeparturedatetime,
               offer.outboundarrivaldatetime, offer.outbounddepartureairport, offer.outbounddeparturedatetime, offer.roomtype,
               offer.hotelid, hotel.hotelname, hotel.hotelstars
        FROM offer
        JOIN hotel ON offer.hotelid = hotel.hotelid
        WHERE outbounddepartureairport IN %s
            AND outbounddeparturedatetime >= %s
            AND inboundarrivaldatetime <= %s
            AND countadults >= %s
            AND countchildren >= %s
            AND (DATE_TRUNC('day', inbounddeparturedatetime) - DATE_TRUNC('day', outbounddeparturedatetime)) = INTERVAL '%s days'
    """

    # check if the hotelid is provided
    if hotelid is not None:
        query += " AND offer.hotelid = %s;"
        params = (tuple(departure_airports), earliest_departure_date, latest_return_date, count_adults, count_children, int(duration), hotelid)
    else:
        query += ";"
        params = (tuple(departure_airports), earliest_departure_date, latest_return_date, count_adults, count_children, int(duration))

    cursor.execute(query, params)

    flights = cursor.fetchall()

    cursor.close()
    return flights

# query to get min prices per hotel
def execute_query_min_prices(departure_airports, earliest_departure_date, latest_return_date, count_adults, count_children, duration):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    query = """
    SELECT o.hotelid, o.outbounddeparturedatetime, o.inbounddeparturedatetime, 
        o.countadults, o.countchildren, o.price, o.inboundarrivaldatetime, 
        o.outbounddepartureairport, o.outboundarrivaldatetime, 
        o.mealtype, o.oceanview, o.roomtype, h.hotelname, h.hotelstars
    FROM (
        SELECT *,
            ROW_NUMBER() OVER (PARTITION BY hotelid ORDER BY price) AS rn
        FROM offer
        WHERE outbounddepartureairport IN %s
            AND outbounddeparturedatetime >= %s
            AND inboundarrivaldatetime <= %s
            AND countadults >= %s
            AND countchildren >= %s
            AND (DATE_TRUNC('day', inbounddeparturedatetime) - DATE_TRUNC('day', outbounddeparturedatetime)) = INTERVAL '%s days'
    ) AS o
    INNER JOIN hotel h ON o.hotelid = h.hotelid
    WHERE o.rn = 1;
    """

    cursor.execute(
        query,
        (tuple(departure_airports), earliest_departure_date, latest_return_date, count_adults, count_children, int(duration))
    )

    flights = cursor.fetchall()
    cursor.close()
    
    return flights

# Search based on list of params. It give the minimum offer per hotel.
# departureAirports, earliestDepartureDate, latestReturnDate, countAdults, countChildren, duration
@app.get('/search')
def search():
    # query params
    params = request.args
    required_params = ["departureAirports", "earliestDepartureDate", "latestReturnDate", "countAdults", "countChildren", "duration"]
    # Check if all required parameters are present
    missing_params = [param for param in required_params if param not in params]

    if missing_params:
        error_message = f"Bad request. Missing required parameters."
        return error_message, 400  # Return error message with status code 400 (Bad Request)
    
    flights = execute_query_min_prices(
        params.getlist("departureAirports"),
        params["earliestDepartureDate"],
        params["latestReturnDate"],
        params["countAdults"],
        params["countChildren"],
        params["duration"],
    )
    
    return flights

# returns all matching offers. 
# By providing the optional query parameter hotelid, you can filter based on a hotel. 
@app.get('/offers')
def search_matching():
    # query params
    params = request.args
    required_params = ["departureAirports", "earliestDepartureDate", "latestReturnDate", "countAdults", "countChildren", "duration"]
    # Check if all required parameters are present
    missing_params = [param for param in required_params if param not in params]

    # optional query param: hotelid
    hotelid = params.get('hotelid')

    if missing_params:
        error_message = f"Bad request. Missing required parameters."
        return error_message, 400  # Return error message with status code 400 (Bad Request)
    
    flights = execute_query_matching(
        params.getlist("departureAirports"),
        params["earliestDepartureDate"],
        params["latestReturnDate"],
        params["countAdults"],
        params["countChildren"],
        params["duration"],
        hotelid
    )
    
    return flights

if __name__ == "__main__":
      app.run(debug=True)  





