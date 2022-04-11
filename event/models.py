import email
from django.db import models
from django.contrib.auth.models import User as MainUser

# Create your models here.


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    contact = models.CharField(unique=True,max_length=12)
    email = models.EmailField()
    street = models.CharField(max_length=124)
    city = models.CharField(max_length=124)
    state = models.CharField(max_length=124)

    def __str__(self):
        return self.name


class EventType(models.Model):
    name = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.name

class Venue(models.Model):
    name = models.CharField(max_length=200,unique=True)
    street = models.CharField(max_length=124)
    city = models.CharField(max_length=124)
    state = models.CharField(max_length=124)
    price_per_day = models.PositiveIntegerField()
    people_accomodate = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class EstimatedPrice(models.Model):
    event_type = models.ForeignKey(EventType,on_delete=models.CASCADE)
    no_of_participants = models.PositiveIntegerField()
    estimation_price = models.PositiveIntegerField()
       
    def __str__(self):
        return self.event_type.name