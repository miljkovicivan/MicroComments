"""
Health check endpoint
"""
from flask import Blueprint

HEALTHCHECK = Blueprint('healthcheck', __name__)


@HEALTHCHECK.route('/comments/health_check')
def healthcheck():
    """
    Returns 200
    """
    return 'OK'
