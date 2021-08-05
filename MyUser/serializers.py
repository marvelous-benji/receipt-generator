from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        #exclude = ['id','is_superuser','is_staff']
        fields = ['email','business_name','fullname']
        extra_kwargs = {'password': {'write_only': True},
                        'fullname':{'write_only':True}
        }
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
        instance.fullname = validated_data.get('fullname', instance.fullname)
        instance.business_name = validated_data.get('business_name', instance.business_name)
        return instance

def generate_access_token(user):
    tokens = RefreshToken.for_user(user)
    return str(tokens.access_token)

#postgres://rfchzxqwfrffhb:d38403b36fbf0c4d6d2a8079035be16f3774a2084f7ed378e701231ed6b15827@ec2-35-168-145-180.compute-1.amazonaws.com:5432/d52f4cuasb6jqi
#python manage.py makemigrations --settings=config.settings.mysettings
