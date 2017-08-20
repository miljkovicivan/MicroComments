FROM python:3.6.1-alpine
ADD . /app
WORKDIR /app

RUN apk update
RUN apk add nginx supervisor gcc musl-dev libc-dev linux-headers

RUN mkdir -p /var/log/uwsgi
RUN touch /var/run/nginx.pid

#RUN echo "daemon off;" >> /etc/nginx/nginx.conf && \
#mkdir -p /var/run/nginx && \
#echo "pid  /var/run/nginx/nginx.pid;" >> /etc/nginx/nginx.conf
#RUN cp /app/nginx.conf /etc/nginx/nginx.conf


RUN pip install -r requirements.txt
CMD ["./docker/run.sh"]
