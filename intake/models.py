from django.db import models
from django.contrib.auth.models import User
from encrypted_model_fields.fields import EncryptedCharField, EncryptedTextField

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = EncryptedCharField(max_length=100)  # Encrypted name field
    email = EncryptedCharField(max_length=255)  # Encrypted email field
    reason = EncryptedTextField()  # Encrypted reason field
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.status}"




# Create your models here.
