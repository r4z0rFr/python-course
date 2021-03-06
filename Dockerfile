FROM python:3
MAINTAINER kaskwoute

USER root

COPY requirements.txt /tmp/requirements.txt

COPY app.py /opt/app.py

RUN pip3 install -r /tmp/requirements.txt

RUN pip3 install requests bs4 nltk spacy-lefff lxml sklearn langdetect

RUN python3 -m spacy download fr
RUN python3 -m spacy download en

WORKDIR /opt

CMD ["python3", "-u", "app.py"]
