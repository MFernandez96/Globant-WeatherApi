FROM python:3.7-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN pip install --upgrade pip

RUN mkdir /requirements/
COPY /requirements/base.txt /requirements/base.txt
RUN pip install -r /requirements/base.txt

COPY . /app
WORKDIR /app

EXPOSE 8000

CMD ["python","manage.py", "runserver", "0.0.0.0:8000"]