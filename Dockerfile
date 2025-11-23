FROM python:3.13.7-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /bank


RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*


RUN pip install pipenv


COPY Pipfile Pipfile.lock ./


RUN pipenv install --deploy --system


COPY . .


EXPOSE 8000
