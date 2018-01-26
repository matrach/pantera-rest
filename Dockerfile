FROM ubuntu:12.04

ADD pantera.list /etc/apt/sources.list.d/pantera.list 
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 21A5DD55
# ssh is required for openmpi to work
RUN apt-get update -y && apt-get install -y pantera ssh python-pip
RUN apt-get install -y python-lxml
RUN pip install flask-restful --index-url=https://pypi.python.org/simple/

RUN locale-gen pl_PL.UTF-8
ENV LC_ALL pl_PL.UTF-8

RUN mkdir /data
WORKDIR /data
COPY api.py /data

#CMD cat >a.txt && pantera a.txt && cat ann_morphosyntax.xml
CMD ["python", "api.py"]
