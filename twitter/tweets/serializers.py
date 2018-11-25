from rest_framework import serializers

from .models import Tweet, Tag


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id', 'name')


class TweetSerializer(serializers.HyperlinkedModelSerializer):
    creator = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
    tags = TagSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Tweet
        fields = ('id', 'text', 'created', 'creator', 'tags')
        read_only_fields = ('id', 'created', 'creator', 'tags')

