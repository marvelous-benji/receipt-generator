from secrets import token_hex
from random import randint

from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from faker import Faker
from loguru import logger

from .serializers import HistorySerializer
from .models import ReceiptHistory
from MyUser.serializers import UserSerializer


fake = Faker()


class ReceiptTemplate(APIView):

    """
    Generates receipt templates for business owners
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def generate_templates(self, user):

        slips = []
        for _ in range(10):
            name = fake.name()
            contact = "+2348" + "".join(fake.ssn().split("-"))
            amount = randint(1000, 100000000)
            date = timezone.now()
            detail = f'{name} bought goods worth {amount} Naira on {date.strftime("%d %b %Y %H:%M:%S")}'
            result = {
                "issued_by": user.business_name,
                "date_issued": date,
                "customer_name": name,
                "customer_phone_number": contact,
                "payment_amount": amount,
                "payment_detail": detail,
            }
            slips.append(result)

        return slips

    def get(self, request):

        try:
            receipts = self.generate_templates(request.user)
            serializers = HistorySerializer(data=receipts, context={"request": request})
            if serializers.is_valid():  # will always be vaild
                serializers.save()
            return Response(
                {"status": "success", "receipts": receipts}, status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(e)
            return Response(
                {"status": "failed", "msg": "An error occured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ReceiptList(APIView):
    """
    Issues receipts  to customers.
    Get lists of all receipt issued
    by a business owner
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, page):

        try:
            issued_receipts = ReceiptHistory.objects.filter(
                issued_by=request.user.id
            ).all()
            page_obj = Paginator(issued_receipts, 100)
            try:
                page_receipt = page_obj.page(page)
                receipts = page_receipt.object_list
                count = len(page_receipt.object_list)
            except (EmptyPage, InvalidPage):
                receipts = []
                count = 0

            serializer = HistorySerializer(receipts, many=True)
            return Response(
                {
                    "status": "success",
                    "count": count,
                    "receipts": serializer.data,
                    "num_pages": page_obj.num_pages,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(e)
            return Response(
                {"status": "failed", "msg": "An error occured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ReceiptDetail(APIView):
    """
    Enables Read, Update and Delete operations
    on receipt histories issued by its business
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_issued_receipt(self, current_user, receipt_id):

        return ReceiptHistory.objects.filter(
            Q(receipt_id=receipt_id) & Q(issued_by=current_user.id)
        ).first()

    def get(self, request, receipt_id):
        try:
            issued_receipt = self.get_issued_receipt(request.user, receipt_id)
            if not issued_receipt:
                return Response(
                    {"status": "failed", "msg": "Receipt not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = HistorySerializer(issued_receipt)
            return Response(
                {"status": "success", "receipts": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(e)
            return Response(
                {"status": "failed", "msg": "An error occured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, receipt_id):

        try:
            data = request.data
            issued_receipt = self.get_issued_receipt(request.user, receipt_id)
            if not issued_receipt:
                return Response(
                    {"status": "failed", "msg": "Receipt not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serialized_data = HistorySerializer(issued_receipt, data=data)
            if serialized_data.is_valid():
                serialized_data.save()

                return Response(
                    {"status": "success", "receipt": serialized_data.data},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"status": "failed", "errors": serialized_data.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error(e)
            return Response(
                {"status": "failed", "msg": "An error occured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, receipt_id):

        try:
            issued_receipt = self.get_issued_receipt(request.user, receipt_id)
            if not issued_receipt:
                return Response(
                    {"status": "failed", "msg": "Receipt not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            issued_receipt.delete()
            return Response(
                {"status": "success", "msg": "Receipt deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(e)
            return Response(
                {"status": "failed", "msg": "An error occured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@api_view(["GET", "POST", "PUT", "DELETE"])
def notfound(request):
    '''
    Forces django to return json url not found response rather than
    spawning HTML 404 error(when DEBUG=True) or blank 500 error(when DEBUG=False)
    '''

    return Response(
        {
            "status": "failed",
            "msg": "URL was not found on the server, check your spellings",
        },
        status=status.HTTP_404_NOT_FOUND,
    )
