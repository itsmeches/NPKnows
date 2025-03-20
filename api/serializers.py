from rest_framework import serializers
from .models import ImageModel
from .models import SensorData
# Define a serializer for the ImageModel, focusing on specific fields
class ImageSerializer(serializers.ModelSerializer):
    # Meta class to specify model and fields for the serializer
    class Meta:
        model = ImageModel
        # Only include the 'image' field in the serialized output
        fields = ['image']

# # Define a serializer for the ImageModel, focusing on specific fields
# class ImageSerializer(serializers.ModelSerializer):
#     # Meta class to specify model and fields for the serializer
#     class Meta:
#         model = ImageModel
#         # Only include the 'image' field in the serialized output
#         fields = ['image']

# Define a serializer for the ImageModel, focusing on specific fields
class ImageSerializer(serializers.ModelSerializer):
    # Adding the image_url to the serialized output to send the full URL of the image
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ImageModel
        fields = ['uuid', 'image', 'image_url', 'prediction_result', 'status', 'created_at']

    # To get the full URL of the image
    def get_image_url(self, obj):
        return obj.image.url if obj.image else None


class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = ['user', 'nitrogen', 'phosphorus', 'potassium', 'timestamp']