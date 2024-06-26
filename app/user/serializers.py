"""
Les serializers en DRF fournissent un mécanisme de validation des données.
En utilisant un UserSerializer, vous pouvez ajouter des validations personnalisées
pour vous assurer que les données reçues
dans les requêtes API sont correctes et complètes avant de les traiter ou de les sauvegarder.
"""


from django.contrib.auth import (
    get_user_model,
    authenticate
)
from django.utils.translation import gettext as _
from rest_framework import serializers
from django.core.validators import RegexValidator
import re

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'first_name']
        extra_kwargs = {'password': {'write_only':True, 'min_length': 5}}

    def validate_username(self, value):
        # Vérifiez que le nom d'utilisateur ne contient que des lettres et des underscores
        if not re.match(r'^[a-z_]+$', value):
            raise serializers.ValidationError("The user name can only contain lower case letters and the '_' character.")
        return value

    #override to user create_user and not just create
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        # recuperer le mdp ou lui assigne None si il n'est pas fourni
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user



class AuthTokenSerializer(serializers.Serializer):

    username = serializers.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[a-z_]+$',
                message= _("The username can only contain lower case letters and the '_' character."),
                code='invalid_username'
            )
        ])
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):

        user = authenticate(
            request=self.context.get('request'),
            username = attrs.get('username'),
            password = attrs.get('password'),
        )

        if not user:
            msg = _('Authentification impossible avec les informations fournis.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs