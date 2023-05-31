# Backend Server with Flask and PostgreSQL

## Project Description
This project implements a backend server using Flask, a lightweight web framework for Python, and PostgreSQL, a powerful open-source relational database management system. The backend serves as the foundation for the application, handling requests from the frontend and interacting with the database to store and retrieve data. It serves the endpoints required by the GenDev Holiday Challenge.

### Prerequisites
The project requires installing Postgresql and Python on your system. 

#### To install PostgreSQL:

1. Open the terminal.
2. Run the following command to install PostgreSQL:
`sudo apt-get install postgresql`

#### To install Python:

1. Open the terminal.
2. Run: 
`sudo apt-get update`
3. Run the following command to install Python:
`sudo apt-get install python3`

Note: this installation process is only for Linux. For Windows or Mac, please check out the respective websites. 

### API Specification
The current version of the application provides two main endpoints: 
/offers - returns a list of matching offers. By providing the hotel id, you can get the matching offers from only one hotel. 
/search - returns a list of lowest matching offers by hotel. 

Both of these endpoints are called by the frontend. 

### Run the application
To run the complete application:
1. Launch the frontend. 
The steps to run the frontend are mentioned in the respective readme. 

2. Launch the backend:
1. Run the following commands to install the requirements:
`pip install -r requirements.txt`
2. Once the requirements are installed, start the server: 
`flask run `
for debugging purposes and for autoreloading, use: `flask run --debug`

### (BONUS FEATURE) Docker
If you would like to save the hassle of installing everything yourself, you can also use the provided Dockerfile. 

### Importing data
In order to use the provided datasets, we use Postgresql for higher query performance. 

1. Create a Postgresql database called "offer"

2. Run the script "init_db.py" in the backend/scripts folder:

`sudo python3 init_db.py`

This will create the "offer" and "hotel" tables. 

3. Log into psql by running (If this is your first time logging in, you need to create a user first. Follow the instructions on the prompt): 

`psql -U <username> -d <database_name>`

4. Once inside, import the hotels.csv dataset (provided in the project) under backend/data.:

`psql -U <username> -d <database_name> -c "\copy hotel FROM 'path/to/csv/file.csv' DELIMITER ',' CSV HEADER";`

Replace the path/to/csv/file.csv with the hotels.csv file. 

5. Now, copy the offers.csv dataset into the offer table:

`psql -U <username> -d <database_name> -c "\copy offer FROM 'path/to/csv/file.csv' DELIMITER ',' CSV HEADER";`

Replace the path/to/csv/file.csv with the offers.csv file. 
**WARNING: since the offers.csv is so large it will take a while to import the dataset into Postgresql. It may take several hours. for me it took 100 minutes.**

### (BONUS FEATURE) Performance Enhancement
In this project, we utilize indexes to enhance the performance of database queries. Indexes are data structures that allow for efficient retrieval of data based on specific columns. By creating indexes on frequently queried columns, we can significantly improve the speed of data retrieval operations.

The benefits of using indexes include:

Faster Query Execution: Indexes enable the database engine to locate the required data more quickly. Instead of scanning the entire table, the database can use the index to locate the relevant rows, reducing the query execution time.

Reduced Disk I/O: Indexes store a subset of the data in a more compact form. This means the database engine needs to read fewer data pages from disk when executing a query, resulting in reduced disk I/O operations and improved overall performance.

Optimized Sorting and Joins: Indexes are instrumental in optimizing sorting and join operations. When performing sorting or joining multiple tables, indexes can be used to minimize the number of comparisons and lookups, leading to faster query execution times.

**In this project query execution performance on my machine increased from 20secs to 100-200ms.**

#### Creating an index
Creating a B-tree index takes about 5-10 minutes on my machine. 

**Create the following indexes for a significant performance boost**

In psql or the pgadmin 4 GUI, run the following SQL commands: 

1. first index:

`CREATE INDEX trip_duration_idx offer(outbounddeparturedatetime, inboundarrivaldatetime, outbounddepartureairport);`

2. second index: 

`CREATE INDEX multiple_col_idx offer(outbounddeparturedatetime, inboundarrivaldatetime, outbounddepartureairport, countadults, countchildren);`

**In order to improve the performance of other queries, new indexes can be created. For example, using the hotelid column or the mealtype and roomtype, if the user decides to search by the roomtype and mealtype**