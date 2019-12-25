FROM python:3.8

RUN mkdir /src

RUN apt-get clean \
    && apt-get -y update

WORKDIR /src
ADD requirements.txt /src
RUN pip install -r requirements.txt
ADD src /src/