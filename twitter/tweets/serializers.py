from rest_framework import serializers

from .models import Tweet, Tag


class TweetSerializer(serializers.HyperlinkedModelSerializer):
    creator = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
    tags = serializers.HyperlinkedRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        view_name='tag-detail'
    )

    class Meta:
        model = Tweet
        fields = ('id', 'url', 'text', 'created', 'creator', 'tags')
        read_only_fields = ('id', 'url', 'created', 'creator')


class TagSerializer(serializers.HyperlinkedModelSerializer):
    associated_tweets = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=True,
        view_name='tweet-detail'
    )

    class Meta:
        model = Tag
        fields = ('id', 'url', 'name', 'associated_tweets')
        read_only_fields = ('id', 'url')
