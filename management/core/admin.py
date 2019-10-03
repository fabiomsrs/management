from django.contrib import admin
from core.models import PaymentRegister, Debt
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.utils.html import format_html
from user.admin import MonthFilter, YearFilter
# Register your models here.


admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(PaymentRegister)
class PaymentRegisterAdmin(admin.ModelAdmin):
	list_display = ('user','paid_value','value_to_be_paid','payment_date')	


@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
	list_display = ('debtor','value','date','pagar_debito')
	search_fields = ('debtor__username',)
	change_list_template = "admin/user/user/change_list.html"
	list_filter = (YearFilter,MonthFilter)

	def pagar_debito(self, obj):
		return format_html(
			'<a href="#" class="button btn-primary payment_debt" id="'+ str(obj.pk) +'">pagar</a>'
		)

	def has_add_permission(self, request, obj=None):		
		return False
	
	def has_change_permission(self, request, obj=None):
		return False

	def get_queryset(self, request):
		import datetime
		date = datetime.datetime.today().date()
		self.month = request.GET.get('month', date.month)
		self.year = request.GET.get('year', date.year)
		qs = super().get_queryset(request)
		if not self.month and not self.self.year:
			return qs
		elif self.year and not self.month:
			return qs.filter(date__year=int(self.year))
		return qs.filter(date__year=int(self.year), date__month=int(self.month))