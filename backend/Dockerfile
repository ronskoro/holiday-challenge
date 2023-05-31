FROM python:3.10-bullseye

COPY . .

RUN pip install -r requirements.txt

# create offer and hotel tables
RUN python3 init_db.py

CMD [ "flask", "run" ]
