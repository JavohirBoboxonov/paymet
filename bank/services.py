from django.db import transaction
from rest_framework.exceptions import ValidationError
from bank.models import BankModel

class PaymentService:
    @staticmethod
    def create_payment(validated_data: dict) -> BankModel:
        payment = BankModel.objects.create(
            order_id=validated_data.get('order_id'),
            amount=validated_data.get('amount'),
            payment_method=validated_data.get('payment_method'),
            status=validated_data.get('status', 'PENDING'),
            transaction_id=validated_data.get('transaction_id'),
            is_deleted=validated_data.get('is_deleted', False)
        )
        return payment

    @staticmethod
    def confirm_payment(payment_id: int) -> BankModel:
        with transaction.atomic():
            try:
                payment = BankModel.objects.select_for_update().get(order_id=payment_id)
            except BankModel.DoesNotExist:
                raise ValidationError({"detail": "Payment not found."})
            if payment.status == 'ACCEPTED':
                raise ValidationError({"detail": "Already accepted payment cannot be confirmed again."})

            if payment.status in ['ACCEPTED', 'REJECTED']:
                raise ValidationError({"detail": "Finalized payment status cannot be changed."})
            payment.status = 'ACCEPTED'
            payment.save()

            return payment