from django.db import models
from apps.base.models import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()


class Speciality(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Specialist(BaseModel):
    full_name = models.CharField(max_length=255)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.full_name} ({self.speciality})"


class Equipment(BaseModel):
    name = models.CharField(max_length=255)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Branch(BaseModel):
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name


class Application(BaseModel):
    STATUS_CHOICES = [
        ("draft", "Qoralama"),
        ("sent", "Yuborildi"),
        ("review", "Ko‘rib chiqilmoqda"),
        ("approved", "Tasdiqlandi"),
        ("rejected", "Rad etildi"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    document_type = models.CharField(max_length=100, null=True, blank=True)
    file = models.FileField(upload_to="applications/files/", null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    app_id = models.CharField(max_length=20, unique=True, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Avtomatik ID berish
        if not self.app_id:
            from uuid import uuid4
            self.app_id = str(uuid4())[:8]  # 8 ta belgadan iborat noyob ID
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ariza {self.app_id} - {self.full_name}"


class ApplicationBranch(BaseModel):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="branches")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    specialities = models.ManyToManyField(Speciality)
    specialists = models.ManyToManyField(Specialist, blank=True)
    equipments = models.ManyToManyField(Equipment, blank=True)\

    def __str__(self):
        return f"{self.application} - {self.branch}"
