

from rest_framework import serializers

from .models import ReceiptHistory
from MyUser.serializers import UserSerializer
from MyUser.models import CustomUser




class HistorySerializer(serializers.ModelSerializer):

	issued_by = UserSerializer()

	class Meta:
	    model = ReceiptHistory
	    fields = [
	    	'receipt_id',
	    	'date_issued',
	    	'issued_by',
	    	'payment_type',
	    	'payment_amount',
	    	'issued_to',
	    	'payment_detail'
	    ]


	def is_valid(self, raise_Exception=False):

		if self.initial_data['payment_type'] not in ['Cash', 'Cheque', 'Bank Transfer']:
			self._errors = {'status':'failed','msg':'Invalid payment type'}
			return False
		amount = self.initial_data['payment_amount'] 
		if not (isinstance(amount, int) or isinstance(amount, float)) and amount <= 0:
			self._errors = {'status':'failed','msg':'Invalid payment amount'}
			return False
		self._validated_data = self.initial_data
		self._errors = {}
		return True

	def create(self, validated_data):
		issued_by = validated_data.pop('issued_by')
		issued_by = CustomUser.objects.get(email=issued_by['email'])
		receipt = ReceiptHistory.objects.create(issued_by=issued_by, **validated_data)
		return receipt

	def update(self, instance, validated_data):

		instance.payment_type = validated_data.get('payment_type', instance.payment_type)
		instance.payment_amount = validated_data.get('payment_amount', instance.payment_amount)
		instance.payment_detail = validated_data.get('payment_detail', instance.payment_detail)
		instance.save()
		return instance

