from django.http import JsonResponse
from rembg import remove
from PIL import Image
import io

def remove_background_view(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            image_file = request.FILES['image']
            image = Image.open(image_file)

            # Process image and remove background
            output_image = remove(image)
            
            # Save the output image to a BytesIO object
            output_io = io.BytesIO()
            output_image.save(output_io, format='PNG')
            output_io.seek(0)

            # Return the modified image as a response
            return JsonResponse({"status": "success", "image": output_io.read().decode('latin1')}, status=200)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "No image provided or incorrect method"}, status=400)
