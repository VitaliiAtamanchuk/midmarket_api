FROM python:3.11-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /celeryworker
COPY ./src ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt
