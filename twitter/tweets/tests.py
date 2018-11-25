from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from twitter.users.models import User


class TestUserViews(TestCase):
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
        self.client = APIClient()
        login_response = self.client.post(reverse('login'), data)
        assert login_response.status_code == 200

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + login_response.data['token'])

    def test_users_list(self):
        r = self.client.get(reverse('user-list'))
        assert r.status_code == 200
        assert len(r.data['results']) == 2

    def test_user_detail(self):
        r = self.client.get(reverse('user-detail', kwargs={'pk': self.user.id}))
        assert r.status_code == 200
        assert r.data['id'] == self.user.id
        assert r.data['is_active'] is True

    def test_user_update(self):
        new_username = 'special_user'
        data = {'username': new_username}
        r = self.client.put(reverse('user-detail', kwargs={'pk': self.user.id}), data=data)
        assert r.status_code == 200
        assert r.data['id'] == self.user.id
        assert r.data['is_active'] is True
        assert r.data['username'] == new_username

    def test_user_delete(self):
        r = self.client.delete(reverse('user-detail', kwargs={'pk': self.user.id}))
        assert r.status_code == 204

    def test_user_delete_non_existent(self):
        r = self.client.delete(reverse('user-detail', kwargs={'pk': 200}))
        assert r.status_code == 404

    def test_user_follow(self):
        r = self.client.put(reverse('user-follow', kwargs={'pk': self.user_famous.id}))
        assert r.status_code == 200
        assert self.user_famous.followers.filter(id=self.user.id).count() == 1

    def test_user_unfollow(self):
        self.user_famous.followers.add(self.user)
        r = self.client.put(reverse('user-unfollow', kwargs={'pk': self.user_famous.id}))
        assert r.status_code == 200
        assert self.user_famous.followers.filter(id=self.user.id).count() == 0

