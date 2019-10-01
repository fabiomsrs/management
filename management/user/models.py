from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.

class User(models.Model):
	first_name = models.CharField(max_length=150, verbose_name='Primeiro Nome')
	username = models.CharField(max_length=30, null=True, blank=True, verbose_name='Usuário')        
	cellphone = models.CharField(max_length=14, null=True, blank=True, verbose_name='Celular')    
	email = models.EmailField(unique=True, verbose_name='E-mail')    
	store_name = models.CharField(max_length=30, null=True, blank=True, verbose_name="Nome da Banca")
	pay_day = models.IntegerField(verbose_name='Dia do mês que é realizado o Pagamento')
	
	def payment_is_overdue(self, month, year):
		date = datetime.today().date()		
		if not self.my_payments.filter(payment_date__year=year,payment_date__month=month).exists() and int(month) != date.month:
			return True
		elif not self.my_payments.filter(payment_date__year=year,payment_date__month=month).exists() and self.pay_day < date.day:
			return True
		return False


	def __str__(self):
		return self.username
	
	class Meta:        
		verbose_name = 'Usuário'
		verbose_name_plural = 'Usuários'