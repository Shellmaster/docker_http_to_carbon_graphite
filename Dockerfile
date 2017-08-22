FROM python:2.7.13-slim
MAINTAINER Rafal S. <rafal@maracje.pl>

ADD Python_Graphite.py /Python_Graphite.py

CMD ["/Python_Graphite.py"]
