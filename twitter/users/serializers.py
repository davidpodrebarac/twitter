from rest_framework import serializers
from .models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    followers = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='user-detail'
    )
    follow = serializers.HyperlinkedIdentityField(
        view_name='user-follow'
    )
    unfollow = serializers.HyperlinkedIdentityField(
        view_name='user-unfollow'
    )

    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'full_name', 'email', 'is_active', 'date_joined', 'followers',
                  'created_tweets', 'follows', 'follow', 'unfollow')
        read_only_fields = ('id', 'url', 'is_active', 'date_joined', 'followers')

