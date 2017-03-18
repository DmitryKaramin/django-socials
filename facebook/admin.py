from django.contrib import admin
import imghdr
import requests


class ArticleAdmin(admin.ModelAdmin):

    def save_related(self, request, form, formsets, change):

        super(ArticleAdmin, self).save_related(request, form, formsets, change)

        for x in form.instance.post_to.all():

            if x.page_id:

                filename = form.instance.picture.name.split("/")[-1]

                payload = {
                    'caption': form.instance.text,
                    'access_token': x.page_access_token
                }

                url = u'https://graph.facebook.com/v2.8/{}/photos'.format(x.page_id)

                with open(form.instance.picture.path, 'rb') as picture:

                    files = [
                                (
                                    'images',
                                    (
                                        filename, picture,
                                        'image/{0}'.format(imghdr.what(form.instance.picture))
                                    )
                                 )
                    ]

                    r = requests.post(url, files=files, data=payload)

                print r.text
                print r.status_code
