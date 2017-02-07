from django.contrib import admin

from .facebook import settings
from .forms import FacebookLoginForm
from .models import FacebookModel, Account
from .facebook.redirect import redirect_to_get_code


class SocialAdmin(admin.ModelAdmin):

    form = FacebookLoginForm

    fields = (
        'email',
        'name',
        'client_id',
        'user_access',
        'pages',
    )

    readonly_fields = (
        'name',
        'user_access',
    )

    @redirect_to_get_code
    def response_post_save_change(self, request, obj):
        redirect_to_model = super(SocialAdmin, self).response_post_save_change(request, obj)
        setattr(settings, "REDIRECT_TO_MODEL", redirect_to_model)

        """
        saves HttpResponceRedirect(URL) for getting back model in admin
        we use it in the view
        """


class ArticlesAdmin(admin.ModelAdmin):
    filter_horizontal = ('facebook_account',)


admin.site.register(FacebookModel, SocialAdmin)
admin.site.register(Account)
