from django.db import models
from django.contrib.auth.models import User
import uuid

class ImageModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(upload_to='images/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate the image with the user
    prediction_result = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the field to now when the object is created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set the field to now every time the object is saved

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f'Image {self.uuid} uploaded by {self.user.username}'
