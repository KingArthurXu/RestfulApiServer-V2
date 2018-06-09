FROM kingarthur/baas
MAINTAINER ArthurXu <qingyu.xu@veritas.com>

ENV BAAS_VERSION=1.0

ADD ./ /baas

VOLUME /baas
EXPOSE 5000
WORKDIR /baas

CMD ["/usr/bin/python", "./runserver.py"]