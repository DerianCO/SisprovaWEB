from django.db import models
from API.Elementos.models import Elemento
from API.Centros.models import Sede
# Create your models here.
from django.contrib.auth.models import User


class Reporte(models.Model):
    fecha_hora_ing = models.DateTimeField(auto_now_add=True)
    sede_rep = models.ForeignKey(Sede,on_delete=models.CASCADE)
    pro_rep = models.ForeignKey(User,on_delete=models.CASCADE)
    fecha_hora_sal = models.DateTimeField(blank=True, null=True)
    class Meta:
        unique_together = (('fecha_hora_ing','pro_rep'),)

    def __str__(self):
        return '{} {} {} {}'.format(self.pro_rep.username,self.sede_rep,self.fecha_hora_ing,self.fecha_hora_sal)


class ElementosReporte(models.Model):
    reporte = models.ForeignKey(Reporte,on_delete=models.CASCADE)
    elemento = models.ForeignKey(Elemento,on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return '{} {} {}'.format(self.status,self.elemento.des_ele,self.reporte.pro_rep.username)
