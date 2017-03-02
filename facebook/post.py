from . import settings
import requests
URL_BODY = getattr(settings, 'URL_BODY')

# SEND_URL = URL_BODY + page_id +'/feed' + ?message="Hello fans"'


def post(func):

    def wrapper(self, *args):

        print 'Wrapper1'

        func(self, *args)

        print 'Wrapper 2'

        print self.post_to.all()

        for x in self.post_to.all():

            print 'Loop'

            if x.page_id:

                payload = {
                    'url': 'http://www.freeiconspng.com/uploads/no-image-icon-3.png',
                    # 'message': self.text,
                    'access_token': x.page_access_token}

                url = u'https://graph.facebook.com/v2.8/{}/photos'.format(x.page_id)

                print url

                r = requests.post(url, data=payload)

                print r.text

        print 'Wrapper 3'

    return wrapper