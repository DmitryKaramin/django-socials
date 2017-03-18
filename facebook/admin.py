from django.contrib import admin
from django.conf import settings
import imghdr

import requests


class ArticleAdmin(admin.ModelAdmin):

    def save_related(self, request, form, formsets, change):

        super(ArticleAdmin, self).save_related(request, form, formsets, change)

        # 'https://upload.wikimedia.org/wikipedia/en/f/f9/No-image-available.jpg'

        for x in form.instance.post_to.all():

            if x.page_id:
                #
                files = form.instance.picture
                # print dir(files.)
                print files.name.split("/")[-1]

                filename = files.name.split("/")[-1]

                payload = {
                    'caption': form.instance.text,
                    'access_token': x.page_access_token
                }

                url = u'https://graph.facebook.com/v2.8/{}/photos'.format(x.page_id)

                print url
                print "image format", imghdr.what(form.instance.picture)
                #
                # with open(form.instance.picture, 'r') as picture:
                #
                files = [
                            (
                                'images',
                                ("No-image-available_HSqc8G9.jpg", open(form.instance.picture.path, 'rb'),
                                'image/{0}'.format(imghdr.what(form.instance.picture)))
                             )
                ]
                #
                r = requests.post(url, files=files, data=payload)
                #
                print r.text
                print r.status_code


# >>> multiple_files = [
#         ('images', ('foo.png', open('foo.png', 'rb'), 'image/png')),
#         ('images', ('bar.png', open('bar.png', 'rb'), 'image/png'))]