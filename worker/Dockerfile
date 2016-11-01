FROM python:2.7

ADD . /worker
WORKDIR /worker
RUN apt-get update
RUN apt-get install git
RUN pip install -r requirements.txt
CMD python -u app.py

