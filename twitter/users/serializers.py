from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }


class UserSerializer(serializers.HyperlinkedModelSerializer):
    followers = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='user-detail'
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'full_name', 'email', 'is_active', 'date_joined', 'followers', 'follows')
        read_only_fields = ('id', 'is_active', 'date_joined', 'followers', 'follows')
        extra_kwargs = {'username': {'required': False}}

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError("A user with that username already exists.")
        return value
