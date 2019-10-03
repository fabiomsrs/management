from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from user.models import User
from core.models import PaymentRegister, Debt
from core.response import UnicodeJsonResponse
import datetime
# Create your views here.

def user_payment(request, pk):
    payment_value = request.POST.get("payment_value")
    year = int(request.POST.get("year"))
    month = int(request.POST.get("month"))
    date = datetime.date(year,month,1)
    try:
        user = User.objects.get(id=pk)
        PaymentRegister.objects.create(user=user, paid_value=payment_value,value_to_be_paid=user.monthly_payment, payment_date=date)
        return UnicodeJsonResponse({"success":True})
    except PaymentRegister.DoesNotExist:
        return UnicodeJsonResponse({"success":False})
    except ValidationError as e:
        return UnicodeJsonResponse({"success":False, "message":"Pagamento já foi realizado esse mês"})
    return UnicodeJsonResponse({"success":False})

def debt_payment(request, pk):
    debt = Debt.objects.get(id=pk)
    payment = debt.payment
    payment.paid_value= payment.value_to_be_paid
    payment.save()
    return UnicodeJsonResponse({"success":True})

