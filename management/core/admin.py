from django.contrib import admin
from core.models import PaymentRegister, Debt
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
# Register your models here.


admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(PaymentRegister)
class PaymentRegisterAdmin(admin.ModelAdmin):
	list_display = ('user','paid_value','value_to_be_paid','payment_date')	


@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
	list_display = ('debtor','value')
	search_fields = ('debtor__username',)

	def has_add_permission(self, request, obj=None):		
		return False
	
	def has_change_permission(self, request, obj=None):
		return False

	# def has_delete_permission(self, request, obj=None):		
	# 	return False		