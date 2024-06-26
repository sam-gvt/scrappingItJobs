

# Views for the user API

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer
)


class CreateUserView(generics.CreateAPIView):
    #new user in the system
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):

    serializer_class = AuthTokenSerializer
    # OPTIONAL
    render_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):

    serializer_class = UserSerializer
    # TokenAuthentication extrait ce jeton (present dans en-tête HTTP 'Authorization') et
    # vérifie s'il est valide et correspond à un utilisateur enregistré.
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # override
    # appelées automatiquement par le framework
    def get_object(self):
        # retrieve and return the authenticated user
        return self.request.user


