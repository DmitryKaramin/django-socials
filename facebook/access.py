from . import settings
from django.conf import settings as project_settings

from django.http import Http404
from django.db import IntegrityError

import requests

URL_TO_FACEBOOK_LOGIN = getattr(settings, 'URL_TO_FACEBOOK_LOGIN')
CLIENT_SECRET = getattr(project_settings, 'CLIENT_SECRET')
ACCESS_TOKEN_URL = getattr(settings, 'ACCESS_TOKEN_URL')
GRAPH_API = getattr(settings, 'GRAPH_API')
PERMISSION_URL = getattr(settings, 'PERMISSION_URL')
DEBUG_URL = getattr(settings, 'DEBUG_URL')

URL_BODY = getattr(settings, 'URL_BODY')


def request_get(url, kwargs=None):
    """
    Chacking request url : returns request data or 404 page error
    :param url: request link
    :param kwargs: params for url request
    :return:
    """

    r = requests.get(url, params=kwargs)

    if r.status_code == 200:
        return r

    else:
        raise Http404


def get_page_access_data(token):

    """
    Change user access token to page access info and data
    :param token: user access token
    :return: token, name, id
    """

    payload = {
        'access_token': token
    }

    page_data = request_get(GRAPH_API, payload)

    for x in page_data.json()['data']:
        i = 0
        while i < len(page_data.json()['data'])-1:
            page_token = x['access_token']
            page_name = x['name']
            page_id = x['id']
            yield page_token, page_name, page_id
            i += 1


def get_user_access_data(code, model):
    """
    Getting user data from data taken from url
    :param code: code taken from redirect url
    :param model: certain facebook model
    :return: json user access data to get token
    """

    redirect_url = getattr(settings, "REDIRECT_URL", None)

    payload = {
        'client_id': model.client_id,
        'redirect_uri': redirect_url,
        'client_secret': CLIENT_SECRET,
        'code': code
    }

    r = request_get(ACCESS_TOKEN_URL, payload)

    return r


def check_publish_page_permission(token):

    """
    Check if we can publish on pages of the account
    :param token: user access token
    :return: True or False
    """

    payload = {
        'access_token': token
    }

    p = request_get(PERMISSION_URL, payload)

    for x in p.json()['data']:
        if x['permission'] == 'publish_pages' and x['status'] == 'granted':
            return True

    return False


def debug_token(kwargs):

    """
    Just checks validation of the page token and when it expires
    :param kwargs: page and user token
    :return: True/False validation and time to expire
    """

    r = request_get(DEBUG_URL, kwargs)

    print "Expires", r.json()['data']['expires_at']
    print "Valid", r.json()['data']['is_valid']
    return r.json()['data']['is_valid'], r.json()['data']['expires_at']


def get_access_token(request, model):

    """
    Main function to get 'access data' and saves it to model
    :param request:
    :param model:
    :return: saves data to model
    """

    client_id = getattr(settings, "CLIENT_ID", None)

    facebook_model = model.objects.get(client_id=client_id)

    code = request.META['QUERY_STRING'].split('=')[1]

    '''If we have user_access Token there is no need to make request'''

    if not facebook_model.user_access_token:

        user_access_token = get_user_access_data(code, facebook_model)
        user_access_token = user_access_token.json()['access_token']
        facebook_model.user_access_token = user_access_token
        print "Facebook pages", facebook_model.pages

    else:

        user_access_token = facebook_model.user_access_token

    if facebook_model.pages:

        for x in facebook_model.pages.all():

            payload = {
                'input_token': x.page_access_token,
                'access_token': facebook_model.user_access_token,
            }

            debug_token(payload)

    publish_permission = check_publish_page_permission(user_access_token)

    if publish_permission:

        """
        using get_page_access_data - generator function
        getting as much pages as exist in account
        """

        for page_token, page_name, page_id in get_page_access_data(user_access_token):

            """
            using try/except construction to check is page already exists
            """

            try:

                payload = {
                    'input_token': page_token,
                    'access_token': facebook_model.user_access_token,
                }

                granted, expires = debug_token(payload)

                facebook_model.pages.create(
                    name=page_name,
                    page_id=page_id,
                    page_access_token=page_token,
                    time_valid=expires,
                    manage_pages_granted=granted,
                )

                facebook_model.save()

            except IntegrityError as e:

                continue
