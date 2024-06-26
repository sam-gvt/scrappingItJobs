from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Alert(models.Model):

    title = models.CharField(max_length=200)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



class Job(models.Model):
    title = models.CharField(max_length=200)
    tjm = models.IntegerField()
    localization = models.CharField(max_length=200)
    experience = models.CharField(max_length=200)
    esn = models.CharField(max_length=200)
    date = models.DateField()
    mission_duration = models.CharField(max_length=200)
    id_alert = models.ForeignKey(Alert, on_delete=models.CASCADE)
    techno = models.ManyToManyField('Techno', related_name='jobs')

    def __str__(self):
        return self.title



class Techno(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name