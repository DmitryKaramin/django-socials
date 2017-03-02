from django.contrib import admin
from django.conf import settings

import requests


class ArticleAdmin(admin.ModelAdmin):

    def save_related(self, request, form, formsets, change):

        super(ArticleAdmin, self).save_related(request, form, formsets, change)

        # 'https://upload.wikimedia.org/wikipedia/en/f/f9/No-image-available.jpg'

        for x in form.instance.post_to.all():

            if x.page_id:

                payload = {
                    'url': 'https://upload.wikimedia.org/wikipedia/en/f/f9/No-image-available.jpg',
                    'caption': form.instance.text,
                    'access_token': x.page_access_token
                }

                url = u'https://graph.facebook.com/v2.8/{}/photos'.format(x.page_id)

                print url

                r = requests.post(url, data=payload)

                print r.text
                print r.status_code
