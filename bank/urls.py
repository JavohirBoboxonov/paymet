from django.urls import path
from .views import (
    PaymentListCreateAPIView, 
    PaymentDetailAPIView, 
    PaymentConfirmAPIView, 
    PaymentWebhookAPIView
)

urlpatterns = [
    path('payments/', PaymentListCreateAPIView.as_view(), name='payment-list-create'),
    path('payments/<int:pk>/', PaymentDetailAPIView.as_view(), name='payment-detail'),
    path('payments/<int:pk>/confirm/', PaymentConfirmAPIView.as_view(), name='payment-confirm'),
    path('payments/webhook/', PaymentWebhookAPIView.as_view(), name='payment-webhook'),
]