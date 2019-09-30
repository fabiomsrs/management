from django.contrib import admin
from django.db.models import Q
from user.models import User
import datetime
from django.utils import timezone
import calendar

# Register your models here.

class YearFilter(admin.SimpleListFilter):	
	title = 'year'
	parameter_name = 'year'

	def lookups(self, request, model_admin):
		return (
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
	list_display = ('first_name','username','em_dias','pagamento_completo','pay_day','store_name')
	list_filter = (IsOverDueFilter,YearFilter,MonthFilter)
	search_fields = ('username', 'first_name')
	year = None
	month = None	
	
	def em_dias(self, obj):		
		return not obj.payment_is_overdue(self.month,self.year)
	
	def pagamento_completo(self, obj):
		if not self.em_dias(obj):
			return False

		for payment in obj.my_payments.all():
			if payment.is_paid_incompletely:
				return False
		return True
	
	def get_queryset(self, request):		
		self.month = request.GET.get('month')
		self.year = request.GET.get('year')
		return super().get_queryset(request)		

	em_dias.boolean = True
	pagamento_completo.boolean = True