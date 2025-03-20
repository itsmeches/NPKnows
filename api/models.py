from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models import Avg


# Define a model to represent an image uploaded by a user, including prediction results and status

# Model to store uploaded images (already in your code)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prediction_result = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
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


# Model to store soil sensor data
class SensorData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_average_npk(user):
        data = SensorData.objects.filter(user=user)
        if not data.exists():
            return {"avg_nitrogen": None, "avg_phosphorus": None, "avg_potassium": None}

        avg_nitrogen = data.aggregate(models.Avg('nitrogen'))['nitrogen__avg']
        avg_phosphorus = data.aggregate(models.Avg('phosphorus'))['phosphorus__avg']
        avg_potassium = data.aggregate(models.Avg('potassium'))['potassium__avg']

        return {"avg_nitrogen": avg_nitrogen, "avg_phosphorus": avg_phosphorus, "avg_potassium": avg_potassium}



# Model for predefined fertilizer recommendations (27 combinations)
class FertilizerRecommendation(models.Model):
    nitrogen_level = models.CharField(max_length=10)
    phosphorus_level = models.CharField(max_length=10)
    potassium_level = models.CharField(max_length=10)
    recommended_rate = models.TextField()

    # Correct field names: Separate Option 1 and Option 2 applications
    option_1_application_1 = models.TextField()
    option_1_application_2 = models.TextField(blank=True, null=True)

    option_2_application_1 = models.TextField()
    option_2_application_2 = models.TextField(blank=True, null=True)

    mode_of_application = models.TextField()
    slightly_acid_loving_crops = models.TextField()  # Ensure this exists

    def __str__(self):
        return f"N:{self.nitrogen_level}, P:{self.phosphorus_level}, K:{self.potassium_level}"
