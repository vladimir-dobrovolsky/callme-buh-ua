FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /app/ && mkdir -p /app/www/static/ && mkdir -p /app/www/media/
WORKDIR /app
COPY app/ /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt