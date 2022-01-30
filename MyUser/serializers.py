from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['email','business_name','fullname','password','business_address']
        extra_kwargs = {'password': {'write_only': True},
                        'fullname':{'write_only':True}
        }
        read_only_fields = ['date_joined']


    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            fullname=validated_data['fullname'],
            business_name=validated_data['business_name'],
            business_address=validated_data['business_address']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.fullname = validated_data.get('fullname', instance.fullname)
        instance.business_name = validated_data.get('business_name', instance.business_name)
        instance.business_address = validated_data.get('business_address', instance.business_address)
        instance.save()
        return instance

def generate_access_token(user):
    tokens = RefreshToken.for_user(user)
    return str(tokens.access_token)
