FROM ubuntu:latest
LABEL description="CYLLIDEIMAGE"
LABEL version="1.0"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
ADD . /flask-app
WORKDIR /flask-app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
