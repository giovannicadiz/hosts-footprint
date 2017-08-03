FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get -y install nmap vim-tiny curl
RUN mkdir /hostfootprint
WORKDIR /hostfootprint
ADD requirements.txt /hostfootprint
RUN pip install -r requirements.txt
ADD . /hostfootprint