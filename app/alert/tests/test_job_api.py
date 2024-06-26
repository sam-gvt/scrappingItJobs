
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Job, Alert

from alert.serializers import (
    JobSerializer,

)

JOB_URL = reverse('alert:job-list')

def url_detail_job(id_job):
    return reverse('alert:job-detail', args=[id_job])


def create_job(alert_instance, **params):
    default = {
        'title':'Django Web developer',
        'tjm':250,
        'localization':'Lyon',
        'experience':'2-3 ans',
        'esn':'Sam company',
        'date':"2024-06-19",
        'mission_duration':'6 mois',
    }

    default.update(**params)
    job = Job.objects.create(id_alert=alert_instance, **default)

    return job

class JobAPITest(TestCase):

    def setUp(self):
        # set up user
        self.user = get_user_model().objects.create_user(username="sam__dev",password="testpass123!")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        # set up alert
        self.alert = Alert.objects.create(id_user=self.user, title='Django')
        self.alert2 = Alert.objects.create(id_user=self.user, title='React')


    def test_create_job(self):

        payload = {
            'title':'Django Web developer',
            'tjm':250,
            'localization':'Lyon',
            'experience':'2-3 ans',
            'esn':'Sam company',
            'date':"2024-06-19",
            'mission_duration':'6 mois',
            'id_alert' : self.alert.id
        }

        res = self.client.post(JOB_URL, payload)


        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['title'], payload['title'])
        self.assertEqual(res.data['id_alert'], self.alert.id)


    def test_get_all_job(self):
        create_job(self.alert)
        create_job(self.alert,**{'title':'PHP 8','localization':'Paris'})

        res = self.client.get(JOB_URL)

        jobs = Job.objects.all().order_by('-id')
        serializer = JobSerializer(jobs, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_get_job(self):
        job = create_job(self.alert)

        url = url_detail_job(job.id)
        res = self.client.get(url)
        serializer = JobSerializer(job)

        self.assertEqual(res.data, serializer.data)


    def test_update_job(self):
        job = create_job(self.alert)

        payload = {
            'title':'Update Title',
            'tjm':345,
            'localization':'Caen',
            'experience':'5 ans',
            'esn':'french tech',
            'date':"2024-06-28",
            'mission_duration':'2 ans',
            'id_alert' : self.alert.id
        }
        url = url_detail_job(job.id)

        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        job.refresh_from_db()

        # user serializer to format date
        serializer_job = JobSerializer(job)
        for key, value in payload.items():
            self.assertEqual(serializer_job.data[key], value)




    def test_partial_update(self):
        job = create_job(self.alert)
        payload = {'title':'partial update'}
        original_tjm = 250
        original_localization = 'Lyon'

        url = url_detail_job(job.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        job.refresh_from_db()
        self.assertEqual(job.title, payload['title'])
        self.assertEqual(job.tjm, original_tjm)
        self.assertEqual(job.localization, original_localization)


    def test_update_alert_returns_error(self):
        pass

    def test_delete_job(self):
        pass

    def test_get_other_users_job_error(self):
        pass

    # completer ces tests
    # ajouter tests en rapport a techno


