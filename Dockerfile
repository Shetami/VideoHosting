FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/VideoHosting

COPY ./req.txt /usr/src/req.txt
RUN pip install -r /usr/src/req.txt

COPY . /usr/src/VideoHosting