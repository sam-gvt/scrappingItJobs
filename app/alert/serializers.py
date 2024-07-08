

from rest_framework import serializers

from core.models import Alert, Job, Techno

class AlertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Alert
        fields = ['id','title', 'id_user']
        read_only_fields = ['id', 'id_user']



class TechnoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Techno
        fields = ['id','name']
        read_only_fields = ['id']

class JobSerializer(serializers.ModelSerializer):

    # many = True because list of objects, not a single object
    technos = TechnoSerializer(many=True, required=False)
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
            'technos'
        ]
        read_only_fields = ['id']

    def _get_or_create_technos(self, technos, job):
        """Handle getting or creating techno as needed."""
        for techno in technos:
            techno_obj, created = Techno.objects.get_or_create(
                **techno,
            )
            job.technos.add(techno_obj)


    def create(self, validated_data):
        """Create a Job"""
        technos = validated_data.pop('technos', [])
        job = Job.objects.create(**validated_data)
        self._get_or_create_technos(technos, job)

        return job
