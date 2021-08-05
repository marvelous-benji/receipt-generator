from datetime import datetime
from secrets import token_hex

from rest_framework import status
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import HistorySerializer
from .models import ReceiptHistory
from MyUser.serializers import UserSerializer


class ReceiptTemplate(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def generate_templates(self,user):

        slips = [
                    {
                    'issued_by':user.business_name,
                    'date_issued':datetime.now(),
                    'issued_to': '',
                    'receipt_id':token_hex(10),
                    'payment_type': '',
                    'payment_amount': 0.00,
                    'payment_detail': ''
                    }
                    for k in range(10)
                ]

        return slips


    def get(self, request):

        try:
             print(request.user)
             return Response(
                    {'status':'success','templates':self.generate_templates(request.user)},
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            print(e)
            return Response(
                    {'status':'failed', 'msg':'An error occured'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )



class ReceiptList(APIView):


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
            print(issued_receipt.receipt_id)
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
            print(issued_receipt)
            if not issued_receipt:
                return Response(
                            {'status':'failed','msg':'Receipt not found'},
                            status=status.HTTP_404_NOT_FOUND
                        )
            issued_receipt.delete()
            return Response(
                        {'status':'success','msg':'Receipt deleted successfully'},
                        status=status.HTTP_204_NO_CONTENT
                    )
        except Exception as e:
            print(e)
            return Response(
                            {'status':'failed','msg':'An error occured'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
