from django.contrib import admin
from django.db.models import Q
from django.utils.html import format_html
from django.utils import timezone
from user.models import User
import datetime
import calendar

# Register your models here.

class YearFilter(admin.SimpleListFilter):	
	title = 'year'
	parameter_name = 'year'

	def lookups(self, request, model_admin):
		return (
			('2021', '2021'),
			('2020', '2020'),
			('2019', '2019'),
			('2018', '2018'),
		)

	def queryset(self, request, queryset):		
		return queryset


class MonthFilter(admin.SimpleListFilter):	
	title = 'month'
	parameter_name = 'month'

	def lookups(self, request, model_admin):
		return (
			(1, 'janeiro'),
			(2, 'fevereiro'),
			(3, 'março'),
			(4, 'abril'),
			(5, 'maio'),
			(6, 'junho'),
			(7, 'julho'),
			(8, 'agosto'),
			(9, 'setembro'),
			(10, 'outubro'),
			(11, 'novembro'),
			(12, 'dezembro'),
		)

	def queryset(self, request, queryset):		
		return queryset


class IsOverDueFilter(admin.SimpleListFilter):
	title = 'em dias'
	parameter_name = 'em_dias'

	def lookups(self, request, model_admin):
		return (
			('Sim', 'Sim'),
			('Nao', 'Nao'),
		)

	def queryset(self, request, queryset):
		value = self.value()
		date = datetime.datetime.today().date()		
		if value == 'Nao':			
			return queryset.filter(~Q(my_payments__payment_date__month=date.month) & Q(pay_day__lt = date.day))
		elif value == 'Sim':
			return queryset.exclude(~Q(my_payments__payment_date__month=date.month) & Q(pay_day__lt = date.day))
		return queryset

 
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('first_name','username','em_dias','pagamento_completo','monthly_payment','pay_day','store_name','pagar')
	list_filter = (IsOverDueFilter,YearFilter,MonthFilter)
	search_fields = ('username', 'first_name')
	change_list_template = "admin/user/user/change_list.html"
	year = None
	month = None

	def pagar(self, obj):
		return format_html(
			'<a href="#" class="button btn-primary payment_button" month='+str(self.month)+' year='+str(self.year)+'>pagar</a>'
		)
	
	def em_dias(self, obj):		
		return not obj.payment_is_overdue(self.month,self.year)
	
	def pagamento_completo(self, obj):
		if not self.em_dias(obj):
			return False

		for payment in obj.my_payments.filter(payment_date__year=self.year, payment_date__month=self.month):
			if payment.is_paid_incompletely:
				return False
		return True
	
	def get_queryset(self, request):
		date = datetime.datetime.today().date()		
		self.month = request.GET.get('month', date.month)
		self.year = request.GET.get('year', date.year)
		date = datetime.date(int(self.year), int(self.month), 1)
		qs = super().get_queryset(request)
		return qs.filter(date_subscription__lte=date)

	em_dias.boolean = True
	pagamento_completo.boolean = True