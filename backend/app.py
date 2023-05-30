from flask import Flask, request
import os
import psycopg2
from dotenv import load_dotenv

app = Flask(__name__)
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
def execute_query_matching(departure_airports, earliest_departure_date, latest_return_date, count_adults, count_children, duration):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor = conn.cursor()

    query = """
    SELECT * from offer
    WHERE 
        outbounddepartureairport IN %s
        AND outbounddeparturedatetime >= %s
        AND inboundarrivaldatetime <= %s
        AND countadults >= %s
        AND countchildren >= %s
        AND (DATE_TRUNC('day', inbounddeparturedatetime) - DATE_TRUNC('day', outbounddeparturedatetime)) = INTERVAL '%s days';
    """

    cursor.execute(
        query,
        (tuple(departure_airports), earliest_departure_date, latest_return_date, count_adults, count_children, int(duration))
    )
    flights = cursor.fetchall()
    cursor.close()
    return flights


# query to get min prices per hotel
def execute_query(departure_airports, earliest_departure_date, latest_return_date, count_adults, count_children, duration):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor = conn.cursor()

    duration_ms = duration * 24 * 60 * 60
    # TODO: the duration could be calculated in different ways. Figure out the right one.
    # TODO: handle the case where the query params are not provided (optional).  
    query = """
    SELECT f.*
    FROM flights f
    INNER JOIN (
        SELECT hotelid, MIN(price) AS lowest_price
        FROM flights
        WHERE
            outbounddepartureairport IN %s
            AND outbounddeparturedatetime >= %s
            AND inboundarrivaldatetime <= %s
            AND countadults >= %s
            AND countchildren >= %s
            AND extract(epoch from (inbounddeparturedatetime - outboundarrivaldatetime)) = %s
        GROUP BY hotelid
    ) AS min_prices
    ON f.hotelid = min_prices.hotelid AND f.price = min_prices.lowest_price
    """

    cursor.execute(
        query,
        (tuple(departure_airports), earliest_departure_date, latest_return_date, count_adults, count_children, duration_ms)
    )
    flights = cursor.fetchall()
    cursor.close()
    return flights

# Search based on list of params:
# departureAirports, earliestDepartureDate, latestReturnDate, countAdults, countChildren, duration
@app.get('/search')
def search():
    # query params
    params = request.args
    flights = execute_query(
        params.getlist("departureAirports"),
        params["earliestDepartureDate"],
        params["latestReturnDate"],
        params["countAdults"],
        params["countChildren"],
        params["duration"]
    )
    
    return flights

# returns all matching offers.
@app.get('/alloffers')
def search_matching():
    # query params
    params = request.args
    required_params = ["departureAirports", "earliestDepartureDate", "latestReturnDate", "countAdults", "countChildren", "duration"]
    # Check if all required parameters are present
    missing_params = [param for param in required_params if param not in params]
    
    if missing_params:
        error_message = f"Bad request. Missing required parameters."
        return error_message, 400  # Return error message with status code 400 (Bad Request)
    
    flights = execute_query_matching(
        params.getlist("departureAirports"),
        params["earliestDepartureDate"],
        params["latestReturnDate"],
        params["countAdults"],
        params["countChildren"],
        params["duration"]
    )
    
    return flights

if __name__ == "__main__":
      app.run(debug=True)  




# @app.route('/test', methods=['GET', 'POST'])
# def search():
#        if request.method == 'POST':
#              if 'username' in request.form:
#                    return request.form['username']
             
#              # check the parameters
#              if request.args.get("username"):
#                 #    return "The user is:" + request.args.get("username")
#                 app.logger.debug('query params given')
#                 return {"hello": 1, "world": 2}
#              return 'no user'
#        else:
#            return 'get method'
       
# @app.post('/user/<path:user_id>')
# def search2(user_id):
#       return f"The user id: {user_id}"

# @app.get('/env-vars')
# def env_vars():
#       return f"{app.config['SQLALCHEMY_DATABASE_URI']}"




