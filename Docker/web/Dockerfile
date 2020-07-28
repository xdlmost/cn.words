FROM alpine:3.7
WORKDIR /webapp
RUN mkdir config app ../local
RUN apk add python3-dev build-base linux-headers pcre-dev
RUN pip3 install uwsgi flask pymysql flask-sqlalchemy
CMD uwsgi --ini /webapp/config/uwsgi.ini

