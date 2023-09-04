from rest_framework.routers import DefaultRouter
from django.urls import path

from users.apps import UsersConfig
from users.views import *

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = (
        [

        ] + router.urls)
