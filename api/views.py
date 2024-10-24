from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ImageSerializer
from .models import ImageModel
import tensorflow as tf
import numpy as np
from PIL import Image
import logging

logger = logging.getLogger(__name__)

# Load the model once at the module level
model = None
try:
    model = tf.keras.models.load_model("C:/Users/hp/bitter_gourd_health/saved_model (1).h5")
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")

def preprocess_image(image_file):
    """Preprocess the image for prediction."""
    try:
        image = Image.open(image_file)
        image = image.resize((299, 299))
        image = np.array(image)

        # Remove alpha channel if present
        if image.shape[-1] == 4:
            image = image[..., :3]

        return np.expand_dims(image, axis=0)

    except Exception as e:
        logger.error(f"Error in preprocessing image: {str(e)}")
        return None

class UserRegistrationView(APIView):
    """API view for user registration."""
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username is already taken'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)

        return Response({'message': 'User registered successfully', 'token': token.key}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    """API view for user login."""
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# Image prediction API
class ImageView(APIView):
    CLASS_NAMES = {
        0: "Healthy",
        1: "Nitrogen Deficient",
        2: "Phosphorus Deficient",
        3: "Potassium Deficient"
    }

    authentication_classes = [TokenAuthentication]  # Specify authentication classes
    permission_classes = [IsAuthenticated]  # Ensure that only authenticated users can access this view

    def post(self, request):
        logger.info("Incoming request data: %s", request.data)  # Log incoming data
        serializer = ImageSerializer(data=request.data)

        if serializer.is_valid():
            image_file = serializer.validated_data['image']
            image_instance = ImageModel(image=image_file, user=request.user)  # Associate image with the user
            image_instance.status = 'PENDING'  # Set initial status
            image_instance.save()  # Save the image instance
            logger.info("Image instance created with UUID: %s, status set to PENDING", image_instance.uuid)  # Log instance creation

            processed_image = preprocess_image(image_file)
            if processed_image is None:
                logger.error("Preprocessing failed for the image.")  # Log the error
                image_instance.status = 'FAILED'  # Update status to 'Failed'
                image_instance.save()  # Save the updated instance
                return Response({"error": "Image preprocessing failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Ensure the model is loaded
            if model is None:
                logger.error("Model not loaded. Cannot proceed with prediction.")
                image_instance.status = 'FAILED'  # Update status to 'Failed'
                image_instance.save()  # Save the updated instance
                return Response({"error": "Model not loaded. Please contact the administrator."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Model prediction
            try:
                logits = model.predict(processed_image)
                logger.info("Raw Predictions (Logits): %s", logits)
            except Exception as e:
                logger.error(f"Prediction error: {str(e)}")
                image_instance.status = 'FAILED'  # Update status to 'Failed'
                image_instance.save()  # Save the updated instance
                return Response({"error": "Prediction failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Prepare the response
            class_index = np.argmax(logits)  # Get the index of the class with the highest score
            max_probability = logits[0][class_index]  # Get the probability of the predicted class
            
            predicted_class = self.CLASS_NAMES.get(class_index, "Unknown")

            # Update the instance with the prediction result and status
            image_instance.prediction_result = predicted_class
            image_instance.status = 'COMPLETED'  # Update status to 'Completed'
            image_instance.save()  # Save the updated instance
            logger.info("Status updated to COMPLETED for image UUID: %s", image_instance.uuid)  # Log the status update

            # Prepare the response
            response_data = {
                'predictions': [{'className': predicted_class, 'probability': float(max_probability) * 100}],  # Convert to percentage
                'predicted_class': predicted_class,
                'confidence': float(max_probability) * 100  # Convert to percentage
            }

            logger.info("Response Data: %s", response_data)  # Log the response
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        # Log serializer errors
        logger.error("Serializer Errors: %s", serializer.errors)  # Log serializer errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)