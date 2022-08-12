# syntax=docker/dockerfile:1

# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# NOTE: all the directives that follow in the Dockerfile will be executed in
# that directory.
WORKDIR /code
COPY requirements.txt /code/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
COPY . /code/