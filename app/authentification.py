'''
Authentication method
'''
# import requests
# from flask import request
from flask_mongorest.authentication import AuthenticationBase


class JwtTokenAuthentication(AuthenticationBase):
    """
    JWT Authentication class
    """
    def authorized(self):
        '''
        This is dummy authorization method.
        Example authentication is commented out.
        '''
        return True
        # from app import APP
        # """
        # Verifies token on rest-api/jwt/login
        # """
        # jwt_token = request.headers.get('Authorization', None)
        # if jwt_token:
            # token = jwt_token.split()[1]
            # authentication_host = APP.config.get('REST_API_HOST')
            # response = requests.post(authentication_host + 'jwt/verify/',
                # data={"token": token}
            # )
            # if response.status_code == 200:
                # return True
        # return False