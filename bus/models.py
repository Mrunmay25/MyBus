from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Bus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    num_of_seats = models.IntegerField()
    num_of_seats_rem = models.IntegerField()
    price = models.IntegerField()
    date = models.DateTimeField()
    time = models.TimeField()

    def get_booked_seats(self):
        booked_seats = Book.objects.filter(busid=self).values_list('num_of_seats', flat=True)
        return booked_seats

class Book(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid')
    busid = models.ForeignKey(Bus, on_delete=models.CASCADE, db_column='busid')
    num_of_seats = models.CharField(max_length=10)