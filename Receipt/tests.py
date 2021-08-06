from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from MyUser.models import CustomUser
from Receipt.models import ReceiptHistory




class Receipt_Test(APITestCase):
    '''
    Unittest and integration tests
    for the receipt api endpoints
    '''

    
    def setUp(self):
        '''
        This setup method helps to generate access tokens
        since all the receipt api endpoints would require
        authentication
        '''


        url = reverse('usersignin')
        CustomUser.objects.create_user('bely@gmail.com','bj',
                                            password='pass_123',
                                            business_name='benji sales')

        data = {'email':'bely@gmail.com', 'password':'pass_123'}

        self.response = self.client.post(url, data, format='json')
        user = CustomUser.objects.get(email='bely@gmail.com')

        ReceiptHistory.objects.create(
                                    issued_to="Mr Test",
                                    payment_type="Cash",
                                    payment_amount=45000,
                                    payment_detail="Bought a washing machine",
                                    receipt_id="t3st1ng",
                                    issued_by=user
                                )



    def test_receipt_templates(self):

        
        url1 = reverse('get_templates')

        token = f"Bearer {self.response.data['access_token']}"

        response1 = self.client.get(url1,  HTTP_AUTHORIZATION=token, format='json')

        self.assertTrue(response1.data['status'], 'success') #  Asserts success response for authenticated users
        self.assertTrue(len(response1.data['templates']), 10) # Asserts that 10 receipts are generated



    def test_issue_receipt(self):

        url = reverse('issued_slips')

        token = f"Bearer {self.response.data['access_token']}"
        data = {
                "issued_to":"Mr test",
                "payment_type":"Cash",
                "payment_amount":4500,
                "payment_detail":"Bought a flash drive"
            }
        response1 = self.client.post(url, data, HTTP_AUTHORIZATION=token, format='json')
        response2 = self.client.get(url, HTTP_AUTHORIZATION=token, format='json')

        self.assertTrue(response1.data['status'], 'success') 
        self.assertNotEqual(response2.data['receipts'], []) # Asserts data persistence


    def test_receipt_edit(self):

        url = reverse('edit_slip',args=('t3st1ng',))
        token = f"Bearer {self.response.data['access_token']}"

        data = {
                'payment_amount':33000,
                'payment_type':'Cheque',
            }

        response1 = self.client.get(url, HTTP_AUTHORIZATION=token, format='json')
        response2 = self.client.put(url, data, HTTP_AUTHORIZATION=token, format='json')
        response3 = self.client.delete(url, HTTP_AUTHORIZATION=token, format='json')
        response4 = self.client.get(url, HTTP_AUTHORIZATION=token, format='json')
        self.assertTrue(response1.data['status'],'success')
        self.assertTrue(response2.data['status'],'success')
        self.assertTrue(response3.status_code,204)
        self.assertTrue(response4.status_code,404)
