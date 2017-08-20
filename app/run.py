"""
Module for running server
"""
import os
from app import APP
from healthcheck import HEALTHCHECK


APP.register_blueprint(HEALTHCHECK)

ENV = os.environ.get('ENV', None)

if ENV == 'local':
    APP.run(host='0.0.0.0', port=1000)
