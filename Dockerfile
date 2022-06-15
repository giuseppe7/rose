FROM python:3
RUN \
  apt-get update && \
  apt-get install ca-certificates && \
  apt-get clean


ADD certs/*.crt /usr/local/share/ca-certificates/
RUN update-ca-certificates

ADD rose.py /
ADD requirements.txt /
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "./rose.py" ]
