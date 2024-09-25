FROM python:3.11-slim

WORKDIR /app

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -y \
    && apt-get install -y wget nano git \
    && apt-get clean

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY ./ .

## EXECUTE
CMD ["python", "dumper.py"]
