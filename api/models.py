from django.db import models
from django.contrib.auth.models import User
import uuid

# Define a model to represent an image uploaded by a user, including prediction results and status
class ImageModel(models.Model):
    # Unique identifier for each image instance, automatically generated and non-editable
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    # Image file field, with images stored in the 'images/' directory
    image = models.ImageField(upload_to='images/')
    
    # Foreign key relationship linking each image to a specific user
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Deletes the image if the user is deleted
    
    # Field to store the result of a prediction for the image, allowing blank values
    prediction_result = models.CharField(max_length=255, null=True, blank=True)
    
    # Timestamp set automatically when a new image instance is created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Timestamp updated each time the image instance is modified
    updated_at = models.DateTimeField(auto_now=True)

    # Choices for the status of an image's processing stage
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),     # Image processing is pending
        ('COMPLETED', 'Completed'), # Image processing is completed
        ('FAILED', 'Failed'),       # Image processing failed
    ]
    # Status field to indicate the processing stage, defaulting to 'PENDING'
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    # Method to provide a string representation of the image instance
    def __str__(self):
        return f'Image {self.uuid} uploaded by {self.user.username}'
