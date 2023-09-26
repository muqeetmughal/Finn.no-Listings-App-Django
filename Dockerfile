FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /django_app
COPY requirements.unix.txt /django_app/
RUN pip install -r requirements.unix.txt
COPY . /django_app/