from rest_framework import serializers
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = USER_MODEL
        fields = ('email', 'password', 'full_name')

        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5,
            }
        }

    def create(self, validated_data):
        """ Create a new user with encrypted password and return it """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
