from django.db import models
class BankModel(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        REJECTED = 'REJECTED', 'Rejected'
        ACCEPTED = 'ACCEPTED', 'Accepted'
    class MethodChoices(models.TextChoices):
        PAYME = 'Payme', 'Payme'
        CLICK = 'Click', 'Click'
        UZUM = 'Uzum', 'Uzum'
    order_id = models.BigIntegerField(unique=True) 
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=30, choices=MethodChoices.choices)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    transaction_id = models.BigIntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return f"Order {self.order_id} - Transaction {self.transaction_id} ({self.status})"