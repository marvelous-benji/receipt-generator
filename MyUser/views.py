from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .models import CustomUser
from .serializers import UserSerializer, generate_access_token




class UserSignup(APIView):

    def post(self, request):
        try:
            data = request.data
            serialized_data = UserSerializer(data=data)
            if serialized_data.is_valid():
                user = serialized_data.save()
                return Response(
                    {'status':'success','msg':'Registration successful'},
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serialized_data.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(e)
            return Response(
                {'status':'failed','msg':'An error occured, check your inputs'},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )


class UserSignin(APIView):

    def post(self, request):
        try:
            data = request.data
            user = authenticate(email=data['email'].lower(), password=data['password'])
            if not user:
                return Response(
                    {'status':'failed','msg':'Incorrect login credentials'},
                    status=status.HTTP_403_FORBIDDEN
                )
            access_token = generate_access_token(user)
            return Response(
                {'status':'success','msg':'Login successful', 'access_token':access_token},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return Response(
                {'status':'failed','msg':'An error occured, check your inputs'},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
