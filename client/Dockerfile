FROM node:7
MAINTAINER Robson Miranda <mirandarfsm@gmail.com>

WORKDIR /tmp/siscalaer

COPY . /tmp/siscalaer

# NGINX #
RUN apt-get update && \
    apt-get install -y nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# NODE #
RUN npm install -g bower
RUN npm install -g grunt-cli
RUN npm install
RUN bower install --allow-root
RUN grunt
RUN cp -r dist/* /var/www/html/

EXPOSE 80

CMD ["/usr/sbin/nginx"]
