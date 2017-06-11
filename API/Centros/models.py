from django.db import models

# Create your models here.
class Centro(models.Model):
    cod_centro = models.CharField(primary_key=True, max_length=3)
    nom_centro = models.CharField(max_length=45)

    def __str__(self):
        return '{}'.format(self.nom_centro)

class Sede(models.Model):
    cod_sede = models.CharField(primary_key=True, max_length=3)
    cod_centro_sede = models.ForeignKey(Centro)
    nom_sede = models.CharField(max_length=45)

    def __str__(self):
        return '{}'.format(self.nom_sede)