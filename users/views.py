from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.serializers import UserSerializer
from users.models import User


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """ Это ViewSet для User """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderator').exists():
            print('.request.user.groups.filter(name="moderator").exists():')
            return User.objects.all()
        # print(self.request.user)

        # пользователь не может видеть список других пользователей
        return User.objects.filter(id=self.request.user.pk)

    def perform_create(self, serializer):
        new_user = serializer.save()
        new_user.save()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
