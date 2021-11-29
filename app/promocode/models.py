from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Promocode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    actual_from = models.DateTimeField()
    actual_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField()

    def save(self, *args, **kwargs):
        now = timezone.now()
        if self.actual_from < now < self.actual_to:
            self.active = True
            super(Promocode, self).save(*args, **kwargs)
        else:
            self.active = False
            super(Promocode, self).save(*args, **kwargs)

    def __str__(self):
        return self.code

