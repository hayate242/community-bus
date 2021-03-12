FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
RUN apt-get update && apt-get install -y \
    default-mysql-client
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD ./wait.sh /tmp/wait.sh