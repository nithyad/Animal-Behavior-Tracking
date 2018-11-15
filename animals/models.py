# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Animal(models.Model):
    animal_type = models.CharField(max_length=50)
    active_time = models.IntegerField()
    non_active_time = models.IntegerField()

    def __str__(self):
        return (str(self.animal_type) + " is active for " + str(self.active_time) + " milliseconds and non active for " + str(self.non_active_time) + " milliseconds.")
