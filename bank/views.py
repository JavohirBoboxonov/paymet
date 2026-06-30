from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from bank.models import BankModel
from .serializer import PaymetPostSerializer
from .services import PaymentService

class PaymentListCreateAPIView(APIView):
    def get(self, request):
        payments = BankModel.objects.filter(is_deleted=False).order_by('-created_at')
        serializer = PaymetPostSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = PaymetPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        PaymentService.create_payment(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
class PaymentDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            payment = BankModel.objects.get(order_id=pk, is_deleted=False)
            serializer = PaymetPostSerializer(payment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BankModel.DoesNotExist:
            return Response({"detail": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)

class PaymentConfirmAPIView(APIView):
    def post(self, request, pk):
        try:
            updated_payment = PaymentService.confirm_payment(payment_id=pk)
            serializer = PaymetPostSerializer(updated_payment)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except BankModel.DoesNotExist:
            return Response({"detail": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PaymentWebhookAPIView(APIView):
    def post(self, request):
        transaction_id = request.data.get('transaction_id')
        if not transaction_id:
            return Response({"error": "transaction_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment = BankModel.objects.get(transaction_id=transaction_id)
            PaymentService.confirm_payment(payment_id=payment.order_id)
            
            return Response({"status": "SUCCESS", "message": "Webhook processed successfully."}, status=status.HTTP_200_OK)
            
        except BankModel.DoesNotExist:
            return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)