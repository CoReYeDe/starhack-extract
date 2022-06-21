FROM python:3.8-alpine

MAINTAINER Waste Watcher

COPY ./src/requirements.txt /app/requirements.txt


WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./src/ /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]