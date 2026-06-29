from rest_framework import serializers
from bank.models import BankModel

class PaymetPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankModel
        fields = '__all__'
    
    def validate_order_id(self, attrs):
        if BankModel.objects.filter(order_id=attrs).exists():
            raise serializers.ValidationError('This Id already used')
        return attrs
    
    def validate_amount(self, data):
        if data <= 1000:
            raise serializers.ValidationError('amount higher must be 1000')
        return data
    
    def validate_status(self, attrs):
        valid_statuses = ['PENDING', 'REJECTED', 'ACCEPTED']
        if attrs == valid_statuses:
            raise serializers.ValidationError('sorry but your entered wrong status')
        
        return attrs
    
    def validate_paymet_method(self, value):
        allowed_methods = ['Paynet', 'Click uz', 'Payme', 'Xalq Banki']
        if value not in allowed_methods:
            raise serializers.ValidationError('Sorry, you entered a wrong payment method')
        return value