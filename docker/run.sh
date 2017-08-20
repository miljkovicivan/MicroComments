#!/bin/sh
if [[ $ENV == 'local' ]]; then
	#statements
	python -u /app/app/run.py
else
	cp /app/nginx.conf /etc/nginx/nginx.conf
	supervisord -n -c /app/supervisor.conf
fi
