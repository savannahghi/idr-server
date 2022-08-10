from knox.views import LoginView as KnoxLoginView
from rest_framework.authentication import BasicAuthentication


class LoginView(KnoxLoginView):
    """The default endpoint for API login."""

    authentication_classes = (BasicAuthentication,)
