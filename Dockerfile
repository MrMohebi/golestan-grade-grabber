FROM joyzoursky/python-chromedriver:3.9-selenium
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "-u", "main.py"]