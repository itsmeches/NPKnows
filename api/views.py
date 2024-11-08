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

# Set up logging for debugging and tracking errors
logger = logging.getLogger(__name__)

# Load the ML model once when the module is imported, to avoid reloading on every request
model = None
try:
    model = tf.keras.models.load_model("C:/Users/hp/bitter_gourd_health/saved_model (1).h5")
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")

def preprocess_image(image_file):
    """Preprocess the uploaded image to prepare it for model prediction."""
    try:
        image = Image.open(image_file)
        image = image.resize((299, 299))  # Resize the image to match model input size
        image = np.array(image)

        # Remove alpha channel if the image has one
        if image.shape[-1] == 4:
            image = image[..., :3]

        # Expand dimensions to simulate a batch
        return np.expand_dims(image, axis=0)

    except Exception as e:
        logger.error(f"Error in preprocessing image: {str(e)}")
        return None

class UserRegistrationView(APIView):
    """API view for handling user registration."""
    def post(self, request):
        # Collect user details from the request data
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Validate required fields
        if not username or not email or not password:
            return Response({'error': 'Username, email, and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the username or email is already taken
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username is already taken'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email is already registered'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create the new user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff = False
            user.is_superuser = False
            user.save()

            # Generate an authentication token for the new user
            token, _ = Token.objects.get_or_create(user=user)

            return Response({'message': 'User registered successfully', 'token': token.key}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    """API view for user login and token generation."""
    def post(self, request):
        # Authenticate user using the provided credentials
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If authenticated, get or create a token
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class ImageView(APIView):
    """API view for image upload and health prediction using the ML model."""
    # Class names corresponding to prediction classes
    CLASS_NAMES = {
        0: "Healthy",
        1: "Nitrogen Deficient",
        2: "Phosphorus Deficient",
        3: "Potassium Deficient"
    }

    # Restrict access to authenticated users only
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logger.info("Incoming request data: %s", request.data)  # Log incoming request data for tracking
        serializer = ImageSerializer(data=request.data)

        if serializer.is_valid():
            image_file = serializer.validated_data['image']
            # Create a new ImageModel instance and associate it with the current user
            image_instance = ImageModel(image=image_file, user=request.user)
            image_instance.status = 'PENDING'  # Set initial status
            image_instance.save()  # Save the instance to the database
            logger.info("Image instance created with UUID: %s, status set to PENDING", image_instance.uuid)

            # Preprocess the image for prediction
            processed_image = preprocess_image(image_file)
            if processed_image is None:
                logger.error("Preprocessing failed for the image.")
                image_instance.status = 'FAILED'  # Mark status as failed
                image_instance.save()
                return Response({"error": "Image preprocessing failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Ensure the model is loaded
            if model is None:
                logger.error("Model not loaded. Cannot proceed with prediction.")
                image_instance.status = 'FAILED'
                image_instance.save()
                return Response({"error": "Model not loaded. Please contact the administrator."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Perform the model prediction
            try:
                logits = model.predict(processed_image)
                logger.info("Raw Predictions (Logits): %s", logits)
            except Exception as e:
                logger.error(f"Prediction error: {str(e)}")
                image_instance.status = 'FAILED'
                image_instance.save()
                return Response({"error": "Prediction failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Interpret the model's output
            class_index = np.argmax(logits)  # Get the index of the class with the highest probability
            max_probability = logits[0][class_index]  # Get the probability of the predicted class
            predicted_class = self.CLASS_NAMES.get(class_index, "Unknown")

            # Update the image instance with the prediction result and mark as completed
            image_instance.prediction_result = predicted_class
            image_instance.status = 'COMPLETED'
            image_instance.save()
            logger.info("Status updated to COMPLETED for image UUID: %s", image_instance.uuid)

            # Structure the response data
            response_data = {
                'predictions': [{'className': predicted_class, 'probability': float(max_probability) * 100}],
                'predicted_class': predicted_class,
                'confidence': float(max_probability) * 100
            }

            logger.info("Response Data: %s", response_data)  # Log response data
            return Response(response_data, status=status.HTTP_201_CREATED)

        # Handle invalid serializer data
        logger.error("Serializer Errors: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
