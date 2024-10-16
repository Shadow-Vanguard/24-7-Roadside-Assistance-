# models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('service_provider', 'Service Provider'),
        
    )
    
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    email = models.EmailField(max_length=150,  db_index=True) 

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    password = models.CharField(max_length=128)  # hashed password
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'phone', 'address','email', 'role']

    def __str__(self):
        return self.username

    class Meta:
        permissions = [
            
        ]
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'
        
    # Fix reverse accessor conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
    )


#tbl_service provider

from django.db import models
from django.conf import settings

# ServiceType model (Admin can add different types of services)
class ServiceType(models.Model):
    servicetype_id = models.AutoField(primary_key=True)
    servicetype_name = models.CharField(max_length=100)

    def __str__(self):
        return self.servicetype_name


# ServiceProvider model (For service providers registering in the system)
from django.conf import settings
from django.db import models

class ServiceProvider(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Reference to CustomUser
    service_type = models.ForeignKey(ServiceType, on_delete=models.SET_NULL, null=True)  # Service type can be null if removed
    certificate = models.ImageField(upload_to='certificates/')  # Certificate upload field
    area_of_service = models.CharField(max_length=255)  # Area of service as text
    location = models.TextField(default='')   # Field to store location details as text
    availability_status = models.BooleanField(default=True)

    def __str__(self):
        # Checks if the service type is available before displaying it
        return f'{self.user.name} - {self.service_type.servicetype_name if self.service_type else "No service type"}'



# Towing Service Model
class TowingService(models.Model):
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)  # Link to ServiceProvider
    vehicle_capacity = models.CharField(max_length=100)  # Capacity of the vehicle
    equipment = models.CharField(max_length=255)  # Equipment used in the towing service

    def __str__(self):
        return f"Towing Service - {self.service_provider.user.name} ({self.service_provider.service_type})"

# Petrol Bunk Service Model
class PetrolBunkService(models.Model):
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)  # Link to ServiceProvider
    fuel_types = models.CharField(max_length=255)  # Types of fuel available
    facilities = models.CharField(max_length=255)  # Additional facilities offered

    def __str__(self):
        return f"Petrol Bunk Service - {self.service_provider.user.name} ({self.service_provider.service_type})"

# Workshop Service Model
class WorkshopService(models.Model):
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)  # Link to ServiceProvider
    speciality = models.CharField(max_length=255)  # Specialization of the workshop
    services_offered = models.CharField(max_length=255)  # List of services offered

    def __str__(self):
        return f"Workshop Service - {self.service_provider.user.name} ({self.service_provider.service_type})"

# Ambulance Service Model
class AmbulanceService(models.Model):
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)  # Link to ServiceProvider
    ambulance_type = models.CharField(max_length=100)  # Type of the ambulance
    ambulance_size = models.CharField(max_length=100)  # Size of the ambulance

    def __str__(self):
        return f"Ambulance Service - {self.service_provider.user.name} ({self.service_provider.service_type})"
    
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ServiceRequest(models.Model):  # Changed from BookingRequest to ServiceRequest
    provider = models.ForeignKey('ServiceProvider', on_delete=models.CASCADE)  # Ensure ServiceProvider is defined elsewhere
    description = models.TextField()
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Service Request from {self.provider.user.name} for {self.description}"  # Updated to reflect new name



from django.db import models
from django.conf import settings
from datetime import datetime

# Booking Model
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Reference to the user making the booking
    service_provider = models.ForeignKey('ServiceProvider', on_delete=models.CASCADE)  # Reference to the service provider
    service_type = models.ForeignKey('ServiceType', on_delete=models.CASCADE)  # The type of service requested
    request_time = models.DateTimeField(default=datetime.now)  # Time of request
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # Status of the booking
    location = models.CharField(max_length=255)  # Location of the service request
    description = models.TextField(blank=True)  # Description of the issue or service needed
    provider_response_time = models.DateTimeField(null=True, blank=True)  # Time when the provider responds

    def __str__(self):
        return f"Booking by {self.user.name} for {self.service_type.servicetype_name} ({self.status})"
