FROM python:3.9.12-bullseye
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
ENV FLASK_APP="api.py"
CMD [ "waitress-serve", "--port=5000" , "api:app"]
