from rest_framework import serializers
from .models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    followers = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='user-detail'
    )

    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'full_name', 'email', 'is_active', 'date_joined', 'followers',
                  'created_tweets')
        read_only_fields = ('id', 'url', 'is_active', 'date_joined', 'followers')

