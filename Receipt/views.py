from datetime import datetime
from secrets import token_hex
from random import randint

from rest_framework import status
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from faker import Faker

from MyUser import serializers

from .serializers import HistorySerializer
from .models import ReceiptHistory
from MyUser.serializers import UserSerializer



fake = Faker()

class ReceiptTemplate(APIView):

    '''
    Generates receipt templates for business owners
    '''

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def generate_templates(self,user):

        slips = []
        for _ in range(10):
            name = fake.name
            contact = fake.country_calling_code()+fake.msisdn()
            amount = randint(1000,100000000)
            date = datetime.utcnow()
            detail = f'{name} bought goods worth {amount} Naira on {date.strftime("%d %b %Y %H:%M:%S")}'
            result = {
                        'issued_by':user.business_name,
                        'date_issued':date,
                        'customer_name':name,
                        'customer_phone_number':contact,
                        'payment_amount': amount,
                        'payment_detail': detail
                    }
            slips.append(result)

        return slips


    def get(self, request):

        try:
            receipts = self.generate_templates(request.user)
            serializers = HistorySerializer(data=receipts,context={'request':request})
            if serializers.is_valid(): # will always be vaild
                serializers.save()
            return Response(
                {'status':'success','receipts':receipts},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return Response(
                    {'status':'failed', 'msg':'An error occured'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )



class ReceiptList(APIView):
    '''
    Issues receipts  to customers.
    Get lists of all receipt issued
    by a business owner
    '''


    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):

        try:
            data = request.data
            data['issued_by'] = UserSerializer(request.user).data
            data['receipt_id'] = token_hex(10)
            serialized_data = HistorySerializer(data=data)
            if serialized_data.is_valid():
                receipt = serialized_data.save()
                return Response(
                        {'status':'success','receipt':serialized_data.data},
                        status=status.HTTP_200_OK
                    )
            return Response(
                    serialized_data.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            print(e)
            return Response(
                    {'status':'failed','msg':'An error occured'},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )

    def get(self, request):

        try:
            issued_receipts = ReceiptHistory.objects.filter(issued_by=request.user.id).all()
            serializer = HistorySerializer(issued_receipts, many=True)
            return Response(
                            {'status':'success','receipts':serializer.data},
                            status=status.HTTP_200_OK
                        )
        except Exception as e:
            print(e)
            return Response(
                            {'status':'failed','msg':'An error occured'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )





class ReceiptDetail(APIView):
    '''
    Enables Read, Update and Delete operations
    on receipt histories issued by its business
    '''


    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get_issued_receipt(self, current_user, receipt_id):

        return ReceiptHistory.objects.filter(
                                            Q(receipt_id=receipt_id) &
                                            Q(issued_by=current_user.id)
                                        ).first()


    def get(self, request, receipt_id):
        try:
            issued_receipt = self.get_issued_receipt(request.user, receipt_id)
            if not issued_receipt:
                return Response(
                            {'status':'failed','msg':'Receipt not found'},
                            status=status.HTTP_404_NOT_FOUND
                        )
            serializer = HistorySerializer(issued_receipt)
            return Response(
                            {'status':'success','receipts':serializer.data},
                            status=status.HTTP_200_OK
                        )
        except Exception as e:
            print(e)
            return Response(
                            {'status':'failed','msg':'An error occured'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )


    def put(self, request, receipt_id):

        try:
            data = request.data
            issued_receipt = self.get_issued_receipt(request.user, receipt_id)
            if not issued_receipt:
                return Response(
                            {'status':'failed','msg':'Receipt not found'},
                            status=status.HTTP_404_NOT_FOUND
                        )
            serialized_data = HistorySerializer(issued_receipt, data=data)
            if serialized_data.is_valid():
                serialized_data.save()

                return Response(
                                {'status':'success','receipt':serialized_data.data},
                                status=status.HTTP_200_OK
                            )

            return Response(
                    serialized_data.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            print(e)
            return Response(
                            {'status':'failed','msg':'An error occured'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )


    def delete(self,request, receipt_id):

        try:
            issued_receipt = self.get_issued_receipt(request.user, receipt_id)
            if not issued_receipt:
                return Response(
                            {'status':'failed','msg':'Receipt not found'},
                            status=status.HTTP_404_NOT_FOUND
                        )
            issued_receipt.delete()
            return Response(
                        {'status':'success','msg':'Receipt deleted successfully'},
                        status=status.HTTP_200_OK
                    )
        except Exception as e:
            print(e)
            return Response(
                            {'status':'failed','msg':'An error occured'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
