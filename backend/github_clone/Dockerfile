# pull official base image
FROM python:3.10.2

# set work directory
WORKDIR /django

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

RUN ["chmod", "+x", "./scripts/wait_for_postgres.sh"]
RUN ["chmod", "+x", "./scripts/start-django.sh"]