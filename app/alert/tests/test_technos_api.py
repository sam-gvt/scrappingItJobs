
from rest_framework.test import APIClient
from rest_framework import status

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from core.models import (
    Job,
    Techno,
)
from alert.serializers import TechnoSerializer


TECHNOS_URL = reverse('alert:techno-list')

def detail_url(techno_id):
    return reverse('alert:techno-detail', args=[techno_id])

def create_user(email='user@example.com', password='testpass123'):
    return get_user_model().objects.create_user(email=email, password=password)



class PublicTechnoAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving tags."""
        res = self.client.get(TECHNOS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)



class PrivateTechnoAPITests(TestCase):

    def setUp(self):
        user_details = {'username':'sam__gvt', 'password':'testpass123!', 'first_name':'Sam'}
        self.user = get_user_model().objects.create_user(**user_details)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)



    def test_create_technos(self):
        payload = {'name':'tailwind css'}
        res = self.client.post(TECHNOS_URL, payload)

    def test_retrieve_technos(self):
        """Test retrieving a list of tags."""
        Techno.objects.create(name='C#')
        Techno.objects.create(name='Python')

        res = self.client.get(TECHNOS_URL)

        technos = Techno.objects.all().order_by('-name')
        serializer = TechnoSerializer(technos, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_update_techno(self):
        techno = Techno.objects.create(name='Wordpress')

        payload = {'name': 'Python'}
        url = detail_url(techno.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        techno.refresh_from_db()
        self.assertEqual(techno.name, payload['name'])

    def test_delete_techno(self):
        techno = Techno.objects.create(name='Wordpress')

        url = detail_url(techno.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Techno.objects.filter(id=techno.id).exists())

