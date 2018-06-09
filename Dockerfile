FROM centos:7
MAINTAINER ArthurXu <qingyu.xu@veritas.com>

ENV BAAS_VERSION=1.0

ADD ./requirements.txt /

RUN yum clean all \
    && yum -y update \
    && yum install -y python-setuptools \
    && easy_install pip \
    && pip install -r /requirements.txt \
        && yum clean all \
        && rm -rf /var/cache/yum \
        && rm -rf /root/.cache

ADD ./ /baas

VOLUME /baas
EXPOSE 5000
WORKDIR /baas

CMD ["/usr/bin/python", "./runserver.py"]