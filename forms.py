from django.forms import ModelForm, PasswordInput
from .models import FacebookModel

class FacebookLoginForm(ModelForm):
    class Meta:
        model = FacebookModel
        widgets = {
            'password': PasswordInput(),
        }
        fields = [
            'name',
            # 'email',
            # 'password',
            'client_id',
            # 'client_secret',
            # 'access_token',
            # 'time_valid',
        ]
