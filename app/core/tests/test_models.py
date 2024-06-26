


from django.test import TestCase
from core import models
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_alert(self):
        user = get_user_model().objects.create_user(
            username = 'sam__gvt',
            password = 'testpass123!',
        )

        alert = models.Alert.objects.create(
            id_user=user,
            title='Django',
        )
        self.assertEqual(str(alert), alert.title)