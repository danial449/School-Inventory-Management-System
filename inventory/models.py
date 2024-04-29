from django.db import models
from account.models import User
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



# Create your models here.
class EquipmentType(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name 
    
class Equipment(models.Model):
    name = models.CharField(max_length=100)
    type=models.ForeignKey(EquipmentType ,on_delete=models.CASCADE , blank=True ,null=True, related_name='equipments') 
    serial_no = models.CharField(max_length=100)
    CPU = models.CharField(max_length=30 , default="N/A")
    GPU = models.CharField(max_length=30 , default="N/A")
    RAM = models.CharField(max_length=30 , default="N/A")
    availability = models.BooleanField(default=True)  
    
    def __str__(self):
        return self.name

class MainEquipment(models.Model):
    DEVICE_STATUS_CHOICES = (
        ('Available', 'Available'),
        ('In Use', 'In Use'),
        ('Under Maintenance', 'Under Maintenance'),
        ('Out of Service', 'Out of Service'),
    )
    
    name = models.CharField(max_length=100)
    type = models.ForeignKey(EquipmentType, on_delete=models.CASCADE, blank=True, null=True, related_name='main_equipments')
    quantity = models.PositiveIntegerField(default=0)
    audit = models.DateField()
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=DEVICE_STATUS_CHOICES, default='Available')
    
    def __str__(self):
        return self.name
    

class Reservation(models.Model):

    STATUS_CHOICES = [
        ('Requested', 'Requested'),
        ('Reserved', 'Reserved'),
        ('Declined', 'Declined'),
        ('Returned', 'Returned'),
    ]

    EQUIPMENT_TYPES = [
        ('Equipment', 'Equipment'),
        ('MainEquipment', 'MainEquipment'),
    ]

    equipment_type = models.CharField(max_length=20, choices=EQUIPMENT_TYPES , default="N/A")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE , null=True , blank=True)
    object_id = models.PositiveIntegerField(null=True , blank=True)
    equipment = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    username = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True)
    reservation_date = models.DateTimeField(default=timezone.now)
    registration_no = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Requested')
    return_date = models.DateTimeField(null=True, blank=True) 

    def __str__(self):
        return f"{self.user.username} - {self.equipment_type}"
    
    