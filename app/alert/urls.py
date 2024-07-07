

from django.urls import path, include
from alert import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('alert', views.AlertViewSet)
router.register('job', views.JobViewSet)
router.register('technos', views.TechnoViewSet)

app_name = 'alert'

urlpatterns = [
    path('', include(router.urls)),
]
