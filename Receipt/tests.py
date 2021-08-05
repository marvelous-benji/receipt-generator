from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from MyUser.models import CustomUser




class Receipt_Test(APITestCase):

    def test_receiptslip(self):
        url0 = reverse('usersignin')
        CustomUser.objects.create_user('bj@gmail.com','bj',password='pass_123', business_name='benji sales')
        data0 = {'email':'bj@gmail.com', 'password':'pass_123'}

        response0 = self.client.post(url0, data0, format='json')

        url1 = reverse('get_slips')
        header = {
            'Authorisation':response0.data['access_token']
        }
        response1 = self.client.get(url1, headers=header, format='json')

        self.assertTrue(response1.status_code, 200)

    def test_issue_receipt(self):
        url0 = reverse('usersignin')
        CustomUser.objects.create_user('bj@gmail.com','bj',password='pass_123', business_name='benji sales')
        data0 = {'email':'bj@gmail.com', 'password':'pass_123'}

        response0 = self.client.post(url0, data0, format='json')

        url1 = reverse('issue_receipt')

        header = {
            'Authorisation':response0.data['access_token']
        }
        data = {
                "issued_to":"Mr test",
                "payment_type":"Card",
                "payment_amount":4500,
                "payment_detail":"Bought a flash drive"
            }
        response1 = self.client.post(url1, data, headers=header, format='json')
        response2 = self.client.get(url1, headers=header, format='json')

        self.assertTrue(response1.status_code, 200)
        self.assertTrue(response2.status_code, 200)
