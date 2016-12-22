from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Line(models.Model):
    text_dep = models.CharField(max_length=100,default="")
    text_arr = models.CharField(max_length=100,default="")
    city_dep = models.CharField(max_length=10)
    city_arr = models.CharField(max_length=10)
    rinko_dep = models.CharField(max_length=10)
    rinko_arr = models.CharField(max_length=10)
    def __str__(self):
        return str(self.id) + ':' + self.text_dep+" to "+self.text_arr
    def __unicode__(self):
        return str(self.id) + ':' + self.text_dep+" to "+self.text_arr
