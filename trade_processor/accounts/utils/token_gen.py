import datetime

import jwt
from django.conf import settings


def generate_access_token(user):
    """
    The generate_access_token function takes in a user object and
     returns an access token.
    The expiry time of this token is set to 20 minutes.

    :param user: Get the username of the user that is currently
        logged in
    :return: A jwt that contains the username of the user
    """

    access_token_payload = {
        'username': user.username,
        'exp': datetime.datetime.utcnow()
        + datetime.timedelta(days=0, minutes=20),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(
        access_token_payload, settings.SECRET_KEY, algorithm='HS256'
    )
    return access_token


def generate_refresh_token(user):
    """
    The generate_refresh_token function generates a refresh token for
     the user.
    The function takes in a user object and returns the refresh token.


    :param user: Get the username of the user
    :return: A refresh token
    """
    refresh_token_payload = {
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow(),
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.SECRET_KEY, algorithm='HS256'
    )
    return refresh_token
