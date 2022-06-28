FROM joyzoursky/python-chromedriver:3.9-selenium
RUN mkdir /app
WORKDIR /app
COPY ./app/ ./
RUN pip install -r requirements.txt

CMD ["python", "main.py"]