FROM python:3.10-slim

WORKDIR /app/flaskAPI/

COPY app.py .

RUN pip install flask

RUN apt-get update

RUN apt install sqlite3 -y

EXPOSE 5000

CMD ["python3", "app.py"]