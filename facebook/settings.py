
URL_TO_FACEBOOK_LOGIN = u"https://www.facebook.com/v2.8/dialog/oauth?client_id={}" \
                        u"&response_type={}" \
                        u"&redirect_uri={}" \
                        u"&scope={}"

URL_BODY = u'https://graph.facebook.com/v2.8/'

ACCESS_TOKEN_URL = URL_BODY + u'oauth/access_token'

PERMISSION_URL = URL_BODY + u'me/permissions'
GRAPH_API = URL_BODY + u'me/accounts'
PAGE_API = URL_BODY + u'me'

DEBUG_URL = URL_BODY + u'debug_token'

# Vars to getattr and setattr
REDIRECT_TO_MODEL = None
CLIENT_ID = None
REDIRECT_URL = None
