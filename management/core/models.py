from django.db import models
# Create your models here.


class Debt(models.Model):
    debtor = models.ForeignKey('user.User', on_delete=models.CASCADE)
    payment = models.ForeignKey('PaymentRegister', on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=30, decimal_places=2, verbose_name='Valor da dívida')    

    class Meta:        
        verbose_name = 'Dívida'
        verbose_name_plural = 'Dívidas'
 

class PaymentRegister(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='my_payments')
    paid_value = models.DecimalField(max_digits=30, decimal_places=2, verbose_name='Valor Pago')
    value_to_be_paid = models.DecimalField(max_digits=30, decimal_places=2, verbose_name='Valor a ser Pago')
    payment_date = models.DateField(verbose_name="Data da efetuação do pagamento")    
    description = models.TextField(null=True, blank=True, verbose_name="descrição do pagamento")

    @property
    def is_paid_incompletely(self):
        if self.paid_value < self.value_to_be_paid:
            return True
        return False 

    def save(self, *args, **kwargs):        
        super(PaymentRegister, self).save(*args, **kwargs)
        if self.is_paid_incompletely:
            Debt.objects.create(debtor=self.user, payment=self, value=self.value_to_be_paid - self.paid_value)
        elif Debt.objects.filter(payment=self) and self.paid_value >= self.value_to_be_paid:
            Debt.objects.filter(payment=self).delete()

    def __str__(self):
        return "Valor pago: " + str(self.paid_value) + " | Valor a ser pago: " + str(self.value_to_be_paid)

    class Meta:        
        verbose_name = 'Registro Pagamento'
        verbose_name_plural = 'Registros de Pagamento'
