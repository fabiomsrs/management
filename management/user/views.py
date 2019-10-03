from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from user.models import User
from core.models import PaymentRegister
from core.response import UnicodeJsonResponse
# Create your views here.

def user_payment(request, pk):
    payment_value = request.POST.get("payment_value")
    try:
        user = User.objects.get(id=pk)
        PaymentRegister.objects.create(user=user, paid_value=payment_value,value_to_be_paid=payment_value)
        return UnicodeJsonResponse({"success":True})
    except PaymentRegister.DoesNotExist:
        return UnicodeJsonResponse({"success":False})
    except ValidationError as e:
        return UnicodeJsonResponse({"success":False, "message":"Pagamento já foi realizado esse mês"})
    return UnicodeJsonResponse({"success":False})
