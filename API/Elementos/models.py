from django.db import models
# Create your models here.
from django.contrib.auth.models import User

class TipoElemento(models.Model):
    cod_tipo_ele = models.CharField(primary_key=True, max_length=3)
    des_tipo_ele = models.CharField(max_length=45)

    def __str__(self):
        return '{}'.format(self.des_tipo_ele)

class Elemento(models.Model):
    cod_ele = models.CharField(primary_key=True, max_length=12)
    cod_tipoele_ele = models.ForeignKey(TipoElemento,on_delete=models.CASCADE)
    des_ele = models.CharField(max_length=75)
    pro_ele = models.ManyToManyField(User)

    def __str__(self):
        return '{}'.format(self.des_ele)
