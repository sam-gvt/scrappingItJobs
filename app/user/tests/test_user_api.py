
from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            'username': 'sam__gvt',
            'password': 'testpass123',
            'first_name' : 'Sam',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(username=payload['username'])

        self.assertTrue(user.check_password(payload['password']))
        # verifie si dans la reponse on ne renvoie pas le password
        self.assertNotIn('password', res.data)


    def test_user_with_username_exists_error(self):
        payload = {
            'username' : 'sam__gvt',
            'password' : 'testpass123',
            'first_name' : 'Sam'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_username_wrong_syntax(self):
        user_details = {
            'username': 'sam@gvt',
            'password': 'password!@',
            'first_name': 'Sam Dev',
        }
        res = self.client.post(CREATE_USER_URL, user_details)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(username=user_details['username']).exists()
        self.assertFalse(user_exists)

    def test_password_too_short_error(self):

        payload = {
            'username' : 'sam__gvt',
            'password' : 'ok',
            'first_name' : 'Sam'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(username=payload['username']).exists()
        self.assertFalse(user_exists)


    def test_create_token_for_user(self):
        user_details = {
            'first_name': 'Sam Dev',
            'username': 'sam__gvt',
            'password': '123'
        }
        create_user(**user_details)

        payload = {
            'username' : user_details['username'],
            'password' : user_details['password']
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        user_details = {
            'first_name': 'Sam Dev',
            'username': 'sam__gvt',
            'password': '123'
        }
        create_user(**user_details)

        payload = {
            'username' : 'wrongsam',
            'password' : user_details['password']
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        user_details = {
            'first_name': 'Sam Dev',
            'username': 'sam__gvt',
            'password': ''
        }
        res = self.client.post(CREATE_USER_URL, user_details)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_retrieve_user_unauthorized(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


####################### PRIVATE USER TESTS ############################

class PrivateUserApiTests(TestCase):

    def setUp(self):
        self.user = create_user(
            username='sam__gvt',
            password='testpass123',
            first_name='Test Name',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


    def test_retrieve_profile_success(self):
        res = self.client.get(ME_URL)

        #self.assertEqual(res.data,{'username': self.user.username, 'first_name': self.user.first_name,})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_me_not_allowed(self):
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        payload = {'first_name':'updated_name', 'password':'newpassword@#'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)






