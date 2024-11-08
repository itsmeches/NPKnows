from rest_framework import serializers
from .models import ImageModel

# Define a serializer for the ImageModel, focusing on specific fields
class ImageSerializer(serializers.ModelSerializer):
    # Meta class to specify model and fields for the serializer
    class Meta:
        model = ImageModel
        # Only include the 'image' field in the serialized output
        fields = ['image']
