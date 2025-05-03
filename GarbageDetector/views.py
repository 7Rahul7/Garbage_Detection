import random
import string
import numpy as np
import os
import tensorflow as tf
import requests
from tensorflow.keras.preprocessing import image
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import login,get_user_model,authenticate,logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from .forms import UploadImageForm
from .models import Profile
from os.path import join
from loguru import logger
from django.http import JsonResponse
# from dotenv import load_dotenv
from decouple import config





ROOT_DIR = settings.BASE_DIR
User = get_user_model()
# load_dotenv()



def get_aqi(request):
    OPENWEATHER_API_KEY= config('OPENWEATHER_API_KEY')
    city = request.GET.get('city', 'Kathmandu')

    try:
        # lat/lon fetch
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={OPENWEATHER_API_KEY}"
        geo_response = requests.get(geo_url)
        logger.info(f"Geo response: {geo_response.text}")
        geo_data = geo_response.json()

        if not geo_data:
            return JsonResponse({"error": "City not found"}, status=404)

        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']

        # AQI data
        aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
        aqi_response = requests.get(aqi_url)
        logger.info(f"AQI response: {aqi_response.text}")
        aqi_data = aqi_response.json()

        aqi_level = aqi_data['list'][0]['main']['aqi']
        aqi_status = {
            1: "Good",
            2: "Fair",
            3: "Moderate",
            4: "Poor",
            5: "Very Poor"
        }.get(aqi_level, "Unknown")

        return JsonResponse({
            "aqi": aqi_level,
            "status": aqi_status
        })

    except Exception as e:
        logger.error(f"AQI fetch failed: {e}")
        return JsonResponse({"error": f"Server error: {str(e)}"}, status=500)

#Otp generation
def generate_otp(length=6):
    characters = string.ascii_letters + string.digits
    otp = ''.join(random.choice(characters) for i in range(length) )
    return otp

def otp_to_mail(email,otp):
    subject = 'Your OTP'
    message = f'Your OTP is: {otp}\nUse this to verification and complete your Registration.'
    send_mail(subject,message, settings.DEFAULT_FROM_EMAIL,[email])
    


#Login
def login_view(request):
    if request.method == "POST":
        try:
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect("dashbaord")
            else:
                return render(request, "signin.html", {"error": "Invalid credentials"})
        except Exception as e:
            logger.error(f"error {e}")

    return render(request, "signin.html")

#logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Register
def register_view(request):
    error = None
    if request.method == "POST":
        try:
            email = request.POST.get("email")
            password = request.POST.get("password")
            username = request.POST.get("username")


            if User.objects.filter(email=email).exists():
                error = "Email already exists."
            else:
                otp = generate_otp()
                request.session["email"] = email
                request.session["password"] = password
                request.session["username"] = username
                request.session["otp"] = otp

                otp_to_mail(email, otp)
                return redirect("verify_otp")  # URL name for OTP verification
        except Exception as e:
            logger.error(f"Error in register_view: {e}")
            error = "Something went wrong. Please try again."

    return render(request, "signup.html", {"error": error})

def verify_otp(request):
    error = None

    if request.method == "POST":
        input_otp = request.POST.get("otp")
        session_otp = request.session.get("otp")
        email = request.session.get("email")
        username = request.session.get("username")
        password = request.session.get("password")

        if not all([session_otp, email, username, password]):
            error = "Session expired. Please register again."
            return render(request, "verify_otp.html", {"error": error})

        if input_otp == session_otp:
            try:
                # if the email already exists
                if User.objects.filter(email=email).exists():
                    error = "Email already registered."
                    return render(request, "verify_otp.html", {"error": error})

                # user creation
                user = User.objects.create_user(username=username, email=email, password=password)

                # manual Backend
                user.backend = 'GarbageDetector.backends.EmailBackend'  # Adjust to your app's path

                login(request, user)

                # Clear session
                for key in ['otp', 'email', 'username', 'password']:
                    request.session.pop(key, None)

                return redirect("login")

            except Exception as e:
                logger.error(f"User creation error: {e}")
                error = "Something went wrong during registration."

        else:
            error = "Invalid OTP. Please try again."

    return render(request, "verify_otp.html", {"error": error})



# Dashboard
@login_required(login_url='login')
def dashboard_view(request):
    return render(request,'dashboard.html')



# According to folder layout.
LABELS = [
    "battery",       
    "biological",    
    "brown-glass",   
    "cardboard",     
    "clothes",       
    "green-glass",   
    "metal",         
    "paper",         
    "plastic",       
    "shoes",         
    "trash",         
    "white-glass"    
]

# According to google and chatgpt
RECYCLABLE = {"brown-glass", "cardboard", "green-glass", "metal", "paper", "plastic", "white-glass"}


model_path = os.path.join(settings.BASE_DIR, 'AI_model/garbage_model_fixed.keras')
model = tf.keras.models.load_model(model_path)

@login_required(login_url='login')
def garbage_predict(request):
    prediction = None
    image_url = None
    form = UploadImageForm()

    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)

        if form.is_valid():
            profile = Profile.objects.get(user=request.user)

            if profile.tokens < 5:
                prediction = "Insufficient tokens. Please recharge."
            else:
                try:
    
                    img_file = request.FILES['file']
                    file_path = default_storage.save(f"temp/{img_file.name}", img_file)
                    img_full_path = os.path.join(settings.MEDIA_ROOT, file_path)
                    image_url = default_storage.url(file_path)

                    img = tf.keras.utils.load_img(img_full_path, target_size=(256, 256))
                    img_array = tf.keras.utils.img_to_array(img)
                    img_batch = tf.expand_dims(img_array, axis=0)

                    pred = model.predict(img_batch)
                    predicted_index = tf.argmax(pred, axis=1).numpy()[0]
                    label = LABELS[predicted_index]
                    status = "Recyclable" if label in RECYCLABLE else "Non-Recyclable"

                    prediction = f"{label.capitalize()} ({status})"

                    # Deduct tokens

                    logger.info(f"Tokens: {profile.tokens}")
                    profile.tokens -= 5
                    profile.save()
                    logger.info(f"Tokens: {profile.tokens}")


                except Exception as e:
                    logger.error(f"Prediction error: {e}")
                    prediction = f"Error: {e}"

    return render(request, 'predict.html', {
        'form': form,
        'prediction': prediction,
        'image_url': image_url,
        'tokens': request.user.profile.tokens if request.user.is_authenticated else None
    })