FROM python:3.8-slim-buster as base

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

FROM base

COPY . .

CMD [ "python3", "app.py"]