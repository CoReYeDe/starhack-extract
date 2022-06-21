FROM ubuntu:16.04

MAINTAINER Waste Watcher

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./src/ /app

WORKDIR /app

RUN pip install -r requirements.txt


ENTRYPOINT [ "python" ]

CMD [ "app.py" ]