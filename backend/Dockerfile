FROM python:3.10-slim

WORKDIR /app/flaskAPI/

COPY app.py .

RUN pip3 install flask

RUN pip3 install mysql-connector-python

RUN apt-get update

RUN apt install sqlite3 -y

EXPOSE 5000

CMD ["python3", "app.py"]