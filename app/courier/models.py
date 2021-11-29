from django.conf import settings
from django.db import models


RATING_CHOICES = [
    (1, "1 - Very bad"),
    (2, "2 - Bad"),
    (3, "3 - Okay"),
    (4, "4 - Great"),
    (5, "5 - Excellent"),
]


class Courier(models.Model):
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    telephone = models.CharField(max_length=12)

    class Meta:
        ordering = ('surname', 'name')
        default_related_name = "courier"

    def __str__(self):
        return self.surname + " " + self.name


class CouriersReview(models.Model):
    order = models.PositiveIntegerField()
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created", )
