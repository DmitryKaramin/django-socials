from .facebook import settings
from .facebook.access import get_access_token
from .models import FacebookModel

# Create your views here.


def function(request):
    get_access_token(request, FacebookModel)

    redirect_to_model = getattr(settings, "REDIRECT_TO_MODEL", None)

    return redirect_to_model
