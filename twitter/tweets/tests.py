from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from twitter.tweets.models import Tweet
from twitter.users.models import User


class TestTweetViews(TestCase):
    def create_user(self, data):
        return User.objects.create_user(**data)

    def setUp(self):
        data = {
            'username': 'test_user',
            'email': 'user@email.com',
            'password': 'banana12',
        }
        self.user = self.create_user(data)
        data_famous = {
            'username': 'famous_user',
            'email': 'very.famous@email.com',
            'password': 'banana12',
        }
        self.user_famous = self.create_user(data_famous)
        data_famous2 = {
            'username': 'famous_user2',
            'email': 'very.famous2@email.com',
            'password': 'banana12',
        }
        self.user_famous2 = self.create_user(data_famous2)
        self.client = APIClient()
        login_response = self.client.post(reverse('login'), data)
        assert login_response.status_code == 200
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + login_response.data['token'])

    def test_tweet_post(self):
        data = {'text': 'This is a #test #post'}
        r = self.client.post(reverse('tweets-list'), data=data)
        assert r.status_code == 201
        assert len(r.data['tags']) == 2
        r = self.client.get(reverse('user-tweets', kwargs={'pk': self.user.id}), data=data)
        assert r.status_code == 200
        assert len(r.data) == 1

    def test_tweet_update(self):
        t = Tweet(creator=self.user, text='This is a #test #post')
        t.save()
        novi_text = 'ovo je #novi tekst'
        r = self.client.put(reverse('tweets-detail', kwargs={'pk': t.id}), data={'text': novi_text})
        assert r.status_code == 200
        assert len(r.data['tags']) == 1

    def test_tweet_destroy(self):
        t = Tweet(creator=self.user, text='This is a #test #post')
        t.save()
        r = self.client.delete(reverse('tweets-detail', kwargs={'pk': t.id}))
        assert r.status_code == 204

    def test_tweet_post_from_subscriber(self):
        "This tests a private timeline"
        t = Tweet(creator=self.user_famous, text='This is a #test #post')
        t.save()
        self.user_famous.followers.add(self.user)
        t2 = Tweet(creator=self.user_famous2, text='This is a #test #post')
        t2.save()
        r = self.client.get(reverse('tweets-list'), data={'subscribed': True})
        assert r.status_code == 200
        assert len(r.data['results']) == 1
        assert r.data['results'][0]['id'] == t.id

