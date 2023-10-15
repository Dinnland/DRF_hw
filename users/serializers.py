from rest_framework import serializers

from users.models import User


# Это сериализатор \/
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # Клиентская сторона не должна иметь возможность отправлять токен вместе с
    # запросом на регистрацию. Сделаем его доступным только на чтение.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        print('create new user:')
        print(validated_data)
        return User.objects.create_user(**validated_data)
