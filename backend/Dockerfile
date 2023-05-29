FROM python:3.10-bullseye
# 1. install the requirements
# 2. run the application
# run the command: flask run

COPY . .

RUN sudo apt-get update \
    sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list' \
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add - \
    sudo apt-get update \
    sudo apt-get -y install postgresql

ENV PG_USERNAME = 'postgres'
ENV PG_PASSWORD = 'password'

RUN pip install -r requirements.txt
RUN python init_db.py

# copy to hotel table
RUN 

# command to copy from a csv: \COPY <table name> FROM 'location + file_name' DELIMITER ',' CSV HEADER;


# Create a user for postgres
# https://www.geeksforgeeks.org/making-a-flask-app-using-a-postgresql-database/

CMD [ "flask", "run" ]
