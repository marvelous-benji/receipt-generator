from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from .models import CustomUser
from .usermanager import CustomUserManager




class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo', fullname='user', business_name='globals')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email='super@user.com', password='foo', fullname='superuser', business_name='globals')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)




class Authentication_Test(APITestCase):

    def test_signup(self):
        url = reverse('usersignup')
        data0 = {'email':'test@test.com','fullname':'test0', 'password':'1234567890', 'business_name':'test sales'}
        data1 = {'email':'', 'fullname':'', 'password':'123456'}

        response0 = self.client.post(url, data0, format='json')
        response1 = self.client.post(url, data1, format='json')

        self.assertEqual(response0.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signin(self):
        url = reverse('usersignin')
        CustomUser.objects.create_user('bj@gmail.com','bj',password='pass_123', business_name='benji sales')
        data0 = {'email':'bj@gmail.com', 'password':'pass_123'}
        data1 = {'email':'bj@gmail.com', 'password':'pas_123'}

        response0 = self.client.post(url, data0, format='json')
        response1 = self.client.post(url, data1, format='json')

        self.assertEqual(response0.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)
