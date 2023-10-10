# pull official base image
FROM python:3.11

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
COPY . /app
WORKDIR /app

# install dependencies
RUN pip install --upgrade pip


RUN pip install -r requirements.txt
EXPOSE 8000