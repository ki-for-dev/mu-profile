FROM python:3.9.13-bullseye

# node install
RUN apt update -y \
    && apt-get install -y nodejs npm

# python
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# npm 
RUN npm install tailwindcss

COPY . .
