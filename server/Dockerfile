FROM python:slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir
RUN pip install gunicorn --no-cache-dir

COPY . .


