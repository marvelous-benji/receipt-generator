from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        exclude = ['is_superuser','is_staff']
        read_only_fields = ['date_joined']

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            fullname=validated_data['fullname'],
            business_name=validated_data.get('business_name','')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.fullname = validated_data.get('content', instance.fullname)
        instance.business_name = validated_data.get('created', instance.business_name)
        return instance



def generate_access_token(user):
    tokens = RefreshToken.for_user(user)
    return str(tokens.access_token)
