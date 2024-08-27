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
    tjm = models.CharField(max_length=200, blank=True, null=True)
    localization = models.CharField(max_length=200, blank=True, null=True)
    experience = models.CharField(max_length=200, blank=True, null=True)
    esn = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    mission_duration = models.CharField(max_length=200,blank=True, null=True)
    contract_type = models.CharField(max_length=200,blank=True, null=True)
    id_alert = models.ForeignKey(Alert, on_delete=models.CASCADE)
    technos = models.ManyToManyField('Techno')

    def __str__(self):
        return self.title



class Techno(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name