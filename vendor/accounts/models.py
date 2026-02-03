from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    CUSTOMER = 'customer'
    VENDOR = 'vendor'

    ROLE_CHOICES = (
        (CUSTOMER, 'Customer'),
        (VENDOR, 'Vendor'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=CUSTOMER
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def is_customer(self):
        return self.role == self.CUSTOMER

    def is_vendor(self):
        return self.role == self.VENDOR
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address_line = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} - {self.city}"
