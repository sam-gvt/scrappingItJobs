

import pprint
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Alert

from alert.serializers import (
    AlertSerializer,
)

ALERT_URL = reverse('alert:alert-list')


def create_alert(user, **params):
    default = {
        'title':'Django',
    }

    default.update(**params)
    alert = Alert.objects.create(id_user=user, **default)

    return alert


class PublicAlertAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):

        res = self.client.get(ALERT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAlertAPITests(TestCase):

    def setUp(self):
        user_details = {'username':'sam__gvt', 'password':'testpass123!', 'first_name':'Sam'}
        self.user = get_user_model().objects.create_user(**user_details)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_only_my_list_alert(self):
        # I can only see my owns alerts
        create_alert(user=self.user, title='Alert for user')

        user2 = get_user_model().objects.create_user(username='user2', password='password12!')
        self.client.force_authenticate(user=user2)
        create_alert(user=user2, title='Alert for user2')

        res = self.client.get(ALERT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_create_alert(self):
        payload = {
            'title': 'Sample Title',
            'id_user': self.user.id
        }
        res = self.client.post(ALERT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        alert = Alert.objects.get(id=res.data['id'])
        self.assertEqual(res.data['title'], alert.title)

    def test_create_alert_with_other_id_user_returns_error(self):

        user2 = get_user_model().objects.create_user(username='user2', password='testpas1234!%')
        self.client.force_authenticate(user=user2)

        payload = {
            'title': 'Sample Title',
            'id_user': self.user.id
        }
        res = self.client.post(ALERT_URL, payload)

        print(res)

    def test_delete_alert(self):

        alert = create_alert(user=self.user)

        url = reverse('alert:alert-detail', args=[alert.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Alert.objects.filter(id=alert.id).exists())


    def test_update_iduser_returns_error(self):
        pass

    def test_update_alert_error(self):
        pass














