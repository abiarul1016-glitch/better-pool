from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    region_code = models.CharField(max_length=50)

    # This is not really needed.
    # specialized_programs = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ParentProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="parent_profile"
    )
    phone_number = models.CharField(max_length=20)
    home_address = models.TextField()
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Child(models.Model):
    parent = models.ForeignKey(
        ParentProfile, on_delete=models.CASCADE, related_name="children"
    )
    first_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(validators=[MinValueValidator(3)])
    school = models.ForeignKey(
        School, on_delete=models.PROTECT, related_name="students"
    )
    program_enrolled = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.first_name} ({self.parent.user.last_name})"


class CarpoolGroup(models.Model):
    name = models.CharField(max_length=150)
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name="carpools"
    )
    driver = models.ForeignKey(
        ParentProfile, on_delete=models.CASCADE, related_name="driving_groups"
    )
    passengers = models.ManyToManyField(
        ParentProfile, related_name="joined_carpools", blank=True
    )
    max_capacity = models.PositiveIntegerField(default=4)
    pickup_time = models.TimeField()
    dropoff_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
