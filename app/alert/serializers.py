

from rest_framework import serializers

from core.models import Alert, Job

class AlertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Alert
        fields = ['id','title', 'id_user']
        read_only_fields = ['id']


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = [
            'title',
            'tjm',
            'localization',
            'experience',
            'esn',
            'date',
            'mission_duration',
            'id_alert',
        ]
        read_only_fields = ['id']

