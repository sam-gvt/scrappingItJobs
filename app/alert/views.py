from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from core.models import Alert, Job, Techno
from .serializers import AlertSerializer, JobSerializer, TechnoSerializer

"""
_NOTE POUR MOI
Utilisez viewsets.ModelViewSet pour des opérations CRUD complètes et standardisées.
Utilisez generics.ListAPIView (et autres vues génériques) pour des actions spécifiques et standard, comme lister ou récupérer des objets.
Utilisez APIView lorsque vous avez besoin de flexibilité maximale et de contrôle total sur les méthodes HTTP et que les vues génériques ou les viewsets ne répondent pas à vos besoins spécifiques.
"""


class AlertViewSet(viewsets.ModelViewSet):
    serializer_class = AlertSerializer
    queryset = Alert.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(
            id_user=self.request.user
        ).order_by('-id').distinct()


    def perform_create(self, serializer):
        serializer.save(id_user=self.request.user)

class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    queryset = Job.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Job.objects.filter(id_alert__id_user=self.request.user).order_by('-id')

class TechnoViewSet(viewsets.ModelViewSet):
    serializer_class = TechnoSerializer
    queryset = Techno.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Techno.objects.order_by('-name')
