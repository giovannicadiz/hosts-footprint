FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get -y install curl vim-tiny
RUN mkdir /global
WORKDIR /global
ADD requirements.txt /global
RUN pip install -r requirements.txt
ADD . /global
