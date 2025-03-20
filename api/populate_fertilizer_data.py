
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bitter_gourd_health.settings')
django.setup()

from api.models import FertilizerRecommendation

# General mode of application and slightly acid loving crops instructions
mode_of_application = """1st Application:  
Mix ½ of recommended Fertilizer with the soil at planting time.  

2nd Application:  
Sidedress with remaining fertilizer when 1st set of fruits begin to form.  

Organic Fertilizer:  
Apply 14 days to 1 month before planting."""

slightly_acid_loving_crops = """Preferred Soil pH between 6.0 and 7.0.  
Use Urea (46-0-0) as a source of N.  
Do not mix lime with organic or inorganic fertilizers."""

# List of all 27 NPK combinations
NPK_COMBINATIONS = [
    {"nitrogen_level": "LOW", "phosphorus_level": "LOW", "potassium_level": "LOW", "recommended_rate": "90 – 80 - 60"},
    {"nitrogen_level": "LOW", "phosphorus_level": "LOW", "potassium_level": "MEDIUM", "recommended_rate": "90 – 80 - 45"},
    {"nitrogen_level": "LOW", "phosphorus_level": "LOW", "potassium_level": "HIGH", "recommended_rate": "90 – 80 - 30"},
    
    {"nitrogen_level": "LOW", "phosphorus_level": "MEDIUM", "potassium_level": "LOW", "recommended_rate": "90 – 65 - 60"},
    {"nitrogen_level": "LOW", "phosphorus_level": "MEDIUM", "potassium_level": "MEDIUM", "recommended_rate": "90 – 65 - 45"},
    {"nitrogen_level": "LOW", "phosphorus_level": "MEDIUM", "potassium_level": "HIGH", "recommended_rate": "90 – 65 - 30"},
    
    {"nitrogen_level": "LOW", "phosphorus_level": "HIGH", "potassium_level": "LOW", "recommended_rate": "90 – 50 - 60"},
    {"nitrogen_level": "LOW", "phosphorus_level": "HIGH", "potassium_level": "MEDIUM", "recommended_rate": "90 – 50 - 45"},
    {"nitrogen_level": "LOW", "phosphorus_level": "HIGH", "potassium_level": "HIGH", "recommended_rate": "90 – 50 - 30"},
    
    {"nitrogen_level": "MEDIUM", "phosphorus_level": "LOW", "potassium_level": "LOW", "recommended_rate": "120 – 80 - 60"},
    {"nitrogen_level": "MEDIUM", "phosphorus_level": "LOW", "potassium_level": "MEDIUM", "recommended_rate": "120 – 80 - 45"},
    {"nitrogen_level": "MEDIUM", "phosphorus_level": "LOW", "potassium_level": "HIGH", "recommended_rate": "120 – 80 - 30"},
    
    {"nitrogen_level": "MEDIUM", "phosphorus_level": "MEDIUM", "potassium_level": "LOW", "recommended_rate": "120 – 65 - 60"},
    {"nitrogen_level": "MEDIUM", "phosphorus_level": "MEDIUM", "potassium_level": "MEDIUM", "recommended_rate": "120 – 65 - 45"},
    {"nitrogen_level": "MEDIUM", "phosphorus_level": "MEDIUM", "potassium_level": "HIGH", "recommended_rate": "120 – 65 - 30"},
    
    {"nitrogen_level": "MEDIUM", "phosphorus_level": "HIGH", "potassium_level": "LOW", "recommended_rate": "120 – 50 - 60"},
    {"nitrogen_level": "MEDIUM", "phosphorus_level": "HIGH", "potassium_level": "MEDIUM", "recommended_rate": "120 – 50 - 45"},
    {"nitrogen_level": "MEDIUM", "phosphorus_level": "HIGH", "potassium_level": "HIGH", "recommended_rate": "120 – 50 - 30"},
    
    {"nitrogen_level": "HIGH", "phosphorus_level": "LOW", "potassium_level": "LOW", "recommended_rate": "150 – 80 - 60"},
    {"nitrogen_level": "HIGH", "phosphorus_level": "LOW", "potassium_level": "MEDIUM", "recommended_rate": "150 – 80 - 45"},
    {"nitrogen_level": "HIGH", "phosphorus_level": "LOW", "potassium_level": "HIGH", "recommended_rate": "150 – 80 - 30"},
    
    {"nitrogen_level": "HIGH", "phosphorus_level": "MEDIUM", "potassium_level": "LOW", "recommended_rate": "150 – 65 - 60"},
    {"nitrogen_level": "HIGH", "phosphorus_level": "MEDIUM", "potassium_level": "MEDIUM", "recommended_rate": "150 – 65 - 45"},
    {"nitrogen_level": "HIGH", "phosphorus_level": "MEDIUM", "potassium_level": "HIGH", "recommended_rate": "150 – 65 - 30"},
    
    {"nitrogen_level": "HIGH", "phosphorus_level": "HIGH", "potassium_level": "LOW", "recommended_rate": "150 – 50 - 60"},
    {"nitrogen_level": "HIGH", "phosphorus_level": "HIGH", "potassium_level": "MEDIUM", "recommended_rate": "150 – 50 - 45"},
    {"nitrogen_level": "HIGH", "phosphorus_level": "HIGH", "potassium_level": "HIGH", "recommended_rate": "150 – 50 - 30"},
]

data = []  # ✅ Define this before the for loop

for comb in NPK_COMBINATIONS:
    data.append({
        "nitrogen_level": comb["nitrogen_level"],
        "phosphorus_level": comb["phosphorus_level"],
        "potassium_level": comb["potassium_level"],
        "recommended_rate": comb["recommended_rate"],
        "option_1_application_1": "10 bags/ha (Organic Fertilizer)\n4.25 bags/ha (14-14-14)\n0.75 bag/ha (46-0-0)\n1.25 bags/ha (0-18-0)",
        "option_1_application_2": "4.25 bags/ha (14-14-14)\n0.75 bag/ha (46-0-0)\n1.25 bags/ha (0-18-0)",
        "option_2_application_1": "10 bags/ha (Organic Fertilizer)\n4.00 bags/ha (16-20-0)\n0.50 bag/ha (46-0-0)\n1.00 bags/ha (0-0-60)",
        "option_2_application_2": "4.00 bags/ha (16-20-0)\n0.50 bags/ha (46-0-0)\n1.00 bag/ha (0-0-60)",
        "mode_of_application": mode_of_application,
        "slightly_acid_loving_crops": slightly_acid_loving_crops
    })


for item in data:
    FertilizerRecommendation.objects.create(
        nitrogen_level=item["nitrogen_level"],
        phosphorus_level=item["phosphorus_level"],
        potassium_level=item["potassium_level"],
        recommended_rate=item["recommended_rate"],
        option_1_application_1=item["option_1_application_1"],
        option_1_application_2=item["option_1_application_2"],
        option_2_application_1=item["option_2_application_1"],
        option_2_application_2=item["option_2_application_2"],
        mode_of_application=item["mode_of_application"],
        slightly_acid_loving_crops=item["slightly_acid_loving_crops"],
    )

print("✅ 27 Fertilizer recommendations successfully added to the database!")
