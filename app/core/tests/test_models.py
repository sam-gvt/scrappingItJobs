


from django.test import TestCase
from core import models
from django.contrib.auth import get_user_model


def create_user(username='sam__gvt', password='testpass123!'):
    """Create a return a new user."""
    return get_user_model().objects.create_user(username, password)

class ModelTests(TestCase):

    def test_create_alert(self):
        user = create_user()

        alert = models.Alert.objects.create(
            id_user=user,
            title='Django',
        )
        self.assertEqual(str(alert), alert.title)


    def test_create_job(self):
        user = create_user()
        alert = models.Alert.objects.create(
            id_user=user,
            title='Django',
        )
        payload = {
            'title':'Django developer',
            'tjm':250,
            'localization':'Lyon',
            'experience':'2-3 ans',
            'esn':'Sam company',
            'date':"2024-06-19",
            'mission_duration':'6 mois',
            'id_alert' : alert,
        }
        job = models.Job.objects.create(**payload)
        self.assertEqual(str(job), job.title)

    def test_create_techno(self):
        techno = models.Techno.objects.create(
            name='Django DRF'
        )

        self.assertEqual(str(techno), techno.name)