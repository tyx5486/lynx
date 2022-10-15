FROM python:3.9.12-bullseye
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt

RUN apt-get update -y
RUN apt-get install cron -y

RUN crontab crontab

CMD python app.py && cron -f 