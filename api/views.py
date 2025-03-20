import time 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import ImageSerializer
from .serial_connection import SerialConnection
from .models import ImageModel
import tensorflow as tf
import numpy as np
from django.http import JsonResponse
from PIL import Image
import logging
from .models import SensorData
from .serializers import SensorDataSerializer
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from serial import SerialException
from django.contrib.auth.decorators import login_required
from .models import FertilizerRecommendation


# Set up logging for debugging and tracking errors
logger = logging.getLogger(__name__)
class ValidateTokenView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"message": "Token is valid"})
    
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])   

def validate_token(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or ' ' not in auth_header:
        return Response({'valid': False, 'error': 'Invalid Authorization header'}, status=401)

    token_key = auth_header.split(' ')[1]
    try:
        token = Token.objects.get(key=token_key)
        user = token.user
        return Response({'valid': True, 'user': {'username': user.username, 'email': user.email}})
    except Token.DoesNotExist:
        return Response({'valid': False}, status=401)


# Set up logging for debugging and tracking errors
logger = logging.getLogger(__name__)



arduino = SerialConnection(port="COM6", baudrate=4800, timeout=1)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def arduino_data(request):
    try:
        data_lines = arduino.read_lines(3)  # Read 3 lines from Arduino
        logger.info("Raw data received from Arduino: %s", data_lines)  # Log raw data

        if not data_lines:
            logger.error("No data received from Arduino")
            return Response({'error': 'No data received from Arduino'}, status=500)

        sensor_data = {}
        for line in data_lines:
            logger.info("Processing line: %s", line)  # Log each line for debugging
            if "Nitrogen:" in line:
                try:
                    sensor_data["nitrogen"] = float(line.split(":")[1].strip().replace(" mg/kg", ""))
                except (IndexError, ValueError) as e:
                    logger.error(f"Error parsing Nitrogen: {e}")
            elif "Phosphorus:" in line:
                try:
                    sensor_data["phosphorus"] = float(line.split(":")[1].strip().replace(" mg/kg", ""))
                except (IndexError, ValueError) as e:
                    logger.error(f"Error parsing Phosphorus: {e}")
            elif "Potassium:" in line:
                try:
                    sensor_data["potassium"] = float(line.split(":")[1].strip().replace(" mg/kg", ""))
                except (IndexError, ValueError) as e:
                    logger.error(f"Error parsing Potassium: {e}")

        if not sensor_data:
            logger.error("No valid sensor data found")
            return Response({'error': 'No valid sensor data found'}, status=500)

        # Save sensor data to the database
        sensor_data_instance = SensorData(
            user=request.user,
            nitrogen=sensor_data.get("nitrogen", 0),
            phosphorus=sensor_data.get("phosphorus", 0),
            potassium=sensor_data.get("potassium", 0)
        )
        sensor_data_instance.save()

        # Serialize the saved data
        serializer = SensorDataSerializer(sensor_data_instance)

        logger.info("Sending response: %s", serializer.data)  # Log the response
        return Response({"sensor_data": serializer.data})

    except SerialException as e:
        logger.error("Error reading serial data: %s", str(e))
        return Response({'error': 'Error reading serial data: {}'.format(str(e))}, status=500)
    except Exception as e:
        logger.error("Error reading Arduino data: %s", str(e))
        return Response({'error': str(e)}, status=500)
























# # Initialize Arduino serial connection
#     # Create a single instance of SerialConnection
# arduino = SerialConnection(port="COM6", baudrate=4800, timeout=1)
# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def arduino_data(request):
#     try:
#         data_lines = arduino.read_lines(3)  # Read 3 lines from Arduino
#         logger.info("Raw data received from Arduino: %s", data_lines)  # Log raw data

#         if not data_lines:
#             logger.error("No data received from Arduino")
#             return Response({'error': 'No data received from Arduino'}, status=500)

#         sensor_data = {}
#         for line in data_lines:
#             logger.info("Processing line: %s", line)  # Log each line for debugging
#             if "Nitrogen:" in line:
#                 try:
#                     sensor_data["nitrogen"] = float(line.split(":")[1].strip().replace(" mg/kg", ""))
#                 except (IndexError, ValueError) as e:
#                     logger.error(f"Error parsing Nitrogen: {e}")
#             elif "Phosphorus:" in line:
#                 try:
#                     sensor_data["phosphorus"] = float(line.split(":")[1].strip().replace(" mg/kg", ""))
#                 except (IndexError, ValueError) as e:
#                     logger.error(f"Error parsing Phosphorus: {e}")
#             elif "Potassium:" in line:
#                 try:
#                     sensor_data["potassium"] = float(line.split(":")[1].strip().replace(" mg/kg", ""))
#                 except (IndexError, ValueError) as e:
#                     logger.error(f"Error parsing Potassium: {e}")

#         if not sensor_data:
#             logger.error("No valid sensor data found")
#             return Response({'error': 'No valid sensor data found'}, status=500)

#         # Save sensor data to the database
#         sensor_data_instance = SensorData(
#             user=request.user,
#             nitrogen=sensor_data.get("nitrogen", 0),
#             phosphorus=sensor_data.get("phosphorus", 0),
#             potassium=sensor_data.get("potassium", 0)
#         )
#         sensor_data_instance.save()

#         # Serialize the saved data
#         serializer = SensorDataSerializer(sensor_data_instance)

#         logger.info("Sending response: %s", serializer.data)  # Log the response
#         return Response({"sensor_data": serializer.data})

#     except SerialException as e:
#         logger.error("Error reading serial data: %s", str(e))
#         return Response({'error': 'Error reading serial data: {}'.format(str(e))}, status=500)
#     except Exception as e:
#         logger.error("Error reading Arduino data: %s", str(e))
#         return Response({'error': str(e)}, status=500)
    
    
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

    @csrf_exempt  # Disable CSRF for testing (remove in production)
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


        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)  # ✅ Proper JSON response
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



def leaf_view(request):
    # Your logic to handle the leaf endpoint, e.g., data processing
    return JsonResponse({'message': 'Leaf data response here!'})


NPK_CATEGORIES = [
    {'name': 'Low N, Low P, Low K', 'nitrogen': 'Low', 'phosphorus': 'Low', 'potassium': 'Low'},
    {'name': 'Low N, Low P, Medium K', 'nitrogen': 'Low', 'phosphorus': 'Low', 'potassium': 'Medium'},
    {'name': 'Low N, Low P, High K', 'nitrogen': 'Low', 'phosphorus': 'Low', 'potassium': 'High'},

    {'name': 'Low N, Medium P, Low K', 'nitrogen': 'Low', 'phosphorus': 'Medium', 'potassium': 'Low'},
    {'name': 'Low N, Medium P, Medium K', 'nitrogen': 'Low', 'phosphorus': 'Medium', 'potassium': 'Medium'},
    {'name': 'Low N, Medium P, High K', 'nitrogen': 'Low', 'phosphorus': 'Medium', 'potassium': 'High'},

    {'name': 'Low N, High P, Low K', 'nitrogen': 'Low', 'phosphorus': 'High', 'potassium': 'Low'},
    {'name': 'Low N, High P, Medium K', 'nitrogen': 'Low', 'phosphorus': 'High', 'potassium': 'Medium'},
    {'name': 'Low N, High P, High K', 'nitrogen': 'Low', 'phosphorus': 'High', 'potassium': 'High'},

    {'name': 'Medium N, Low P, Low K', 'nitrogen': 'Medium', 'phosphorus': 'Low', 'potassium': 'Low'},
    {'name': 'Medium N, Low P, Medium K', 'nitrogen': 'Medium', 'phosphorus': 'Low', 'potassium': 'Medium'},
    {'name': 'Medium N, Low P, High K', 'nitrogen': 'Medium', 'phosphorus': 'Low', 'potassium': 'High'},

    {'name': 'Medium N, Medium P, Low K', 'nitrogen': 'Medium', 'phosphorus': 'Medium', 'potassium': 'Low'},
    {'name': 'Medium N, Medium P, Medium K', 'nitrogen': 'Medium', 'phosphorus': 'Medium', 'potassium': 'Medium'},
    {'name': 'Medium N, Medium P, High K', 'nitrogen': 'Medium', 'phosphorus': 'Medium', 'potassium': 'High'},

    {'name': 'Medium N, High P, Low K', 'nitrogen': 'Medium', 'phosphorus': 'High', 'potassium': 'Low'},
    {'name': 'Medium N, High P, Medium K', 'nitrogen': 'Medium', 'phosphorus': 'High', 'potassium': 'Medium'},
    {'name': 'Medium N, High P, High K', 'nitrogen': 'Medium', 'phosphorus': 'High', 'potassium': 'High'},

    {'name': 'High N, Low P, Low K', 'nitrogen': 'High', 'phosphorus': 'Low', 'potassium': 'Low'},
    {'name': 'High N, Low P, Medium K', 'nitrogen': 'High', 'phosphorus': 'Low', 'potassium': 'Medium'},
    {'name': 'High N, Low P, High K', 'nitrogen': 'High', 'phosphorus': 'Low', 'potassium': 'High'},

    {'name': 'High N, Medium P, Low K', 'nitrogen': 'High', 'phosphorus': 'Medium', 'potassium': 'Low'},
    {'name': 'High N, Medium P, Medium K', 'nitrogen': 'High', 'phosphorus': 'Medium', 'potassium': 'Medium'},
    {'name': 'High N, Medium P, High K', 'nitrogen': 'High', 'phosphorus': 'Medium', 'potassium': 'High'},

    {'name': 'High N, High P, Low K', 'nitrogen': 'High', 'phosphorus': 'High', 'potassium': 'Low'},
    {'name': 'High N, High P, Medium K', 'nitrogen': 'High', 'phosphorus': 'High', 'potassium': 'Medium'},
    {'name': 'High N, High P, High K', 'nitrogen': 'High', 'phosphorus': 'High', 'potassium': 'High'},
]


def classify_npk_level(nitrogen, phosphorus, potassium):
    """Classify the NPK values into Low, Medium, or High based on given ranges."""
    def classify_n(n):
        if n < 10:
            return "LOW"
        elif 10 <= n <= 20:
            return "MEDIUM"
        else:
            return "HIGH"

    def classify_p(p):
        if p <= 15:
            return "LOW"
        elif 16 <= p <= 25:
            return "MEDIUM"
        else:
            return "HIGH"

    def classify_k(k):
        if k < 60:
            return "LOW"
        elif 61 <= k <= 130:
            return "MEDIUM"
        else:
            return "HIGH"

    return classify_n(nitrogen), classify_p(phosphorus), classify_k(potassium)

def find_closest_npk_category(avg_npk):
    """Find the closest NPK category based on classification."""
    classified_n, classified_p, classified_k = classify_npk_level(
        avg_npk['avg_nitrogen'], avg_npk['avg_phosphorus'], avg_npk['avg_potassium']
    )

    for category in NPK_CATEGORIES:
        if (
            category['nitrogen'] == classified_n and
            category['phosphorus'] == classified_p and
            category['potassium'] == classified_k
        ):
            return category

    return None  # Return None if no exact match is found


# @login_required
@csrf_exempt  # This disables CSRF for this view
def get_recommendation(request):
    n = request.GET.get("n", "").strip().upper()
    p = request.GET.get("p", "").strip().upper()
    k = request.GET.get("k", "").strip().upper()

    print(f"Querying for NPK: {n}, {p}, {k}")  # Debugging line

    try:
        rec = FertilizerRecommendation.objects.get(
            nitrogen_level=n,
            phosphorus_level=p,
            potassium_level=k,
        )
        return JsonResponse({
            "Combination": f"{rec.nitrogen_level} N, {rec.phosphorus_level} P, {rec.potassium_level} K",
            "Fertilizer Recommended Rate": rec.recommended_rate,
            "Option 1 - 1st Application": rec.option_1_application_1,
            "Option 1 - 2nd Application": rec.option_1_application_2,
            "Option 2 - 1st Application": rec.option_2_application_1,
            "Option 2 - 2nd Application": rec.option_2_application_2,
            "Mode of Application": rec.mode_of_application,
            "Slightly Acid Loving Crops": rec.slightly_acid_loving_crops,
        })
    except FertilizerRecommendation.DoesNotExist:
        print("No matching recommendation found!")  # Debugging line
        return JsonResponse({"error": "No recommendation found for this NPK combination."})
    
    
    
    

    
    
    
    
    