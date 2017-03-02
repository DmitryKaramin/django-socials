from django.shortcuts import reverse
from django.http import HttpResponseRedirect

from . import settings

URL_TO_FACEBOOK_LOGIN = getattr(settings, 'URL_TO_FACEBOOK_LOGIN')


def get_redirect_url(obj, request):
    """
    Constructs url for redirection to get 'code'
    :param obj:
    :param request:
    :return: URL
    """

    redirect_url = reverse('socials:login')
    http_origin = request.META['HTTP_ORIGIN']
    redirect_url = http_origin + redirect_url
    # constructs URL to the view to

    setattr(settings, "REDIRECT_URL", redirect_url)
    setattr(settings, "CLIENT_ID", obj.client_id)
    # saves REDIRECT_URL and CLIENT_ID for further usage of it's values

    return redirect_url


def redirect_to_get_code(func):
    """
    Decorator for ModelAdmin method.
    Overrides redirect. It goes to Facebook for login and grant access
    with permission in 'scope'. As a result we get 'code' in 'redirect_url' URL
    :param func:
    :return: Redirect to Facebook
    """

    def wrapper(inst, request, obj):

        redirect_url = get_redirect_url(obj, request)

        payload = {
            'client_id': obj.client_id,
            'response_type': 'code',
            'redirect_uri': redirect_url,
            'scope': 'manage_pages, publish_pages, pages_show_list, user_photos, publish_actions'
        }

        url = URL_TO_FACEBOOK_LOGIN.format(
            payload['client_id'],
            payload['response_type'],
            payload['redirect_uri'],
            payload['scope']
        )

        func(inst, request, obj)

        return HttpResponseRedirect(url)

    return wrapper
