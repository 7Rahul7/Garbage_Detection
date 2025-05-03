import random
import string
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import login
from .forms import UploadImageForm
from os.path import join
from loguru import logger




ROOT_DIR = settings.BASE_DIR


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
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
    if user:
        login(request, user)
        return redirect(name=dashboard_view)
    return render(request, 'signin.html')


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
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                login(request, user)
                # Clean up session
                del request.session['otp']
                del request.session['email']
                del request.session['username']
                del request.session['password']
                return redirect("dashboard_view")  # or 'dashboard' if you use name in urls.py
            except Exception as e:
                logger.error(f"User creation error: {e}")
                error = "Something went wrong during registration."
        else:
            error = "Invalid OTP. Please try again."

    return render(request, "verify_otp.html", {"error": error})


# Dashboard
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


def garbage_predict(request):
    prediction = None
    image_url = None
    form = UploadImageForm()

    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                # Save the uploaded image to media/temp/
                img_file = request.FILES['file']
                logger.info(img_file)
                file_path = default_storage.save(f"temp/{img_file.name}", img_file)
                logger.info(file_path)
                img_full_path = os.path.join(settings.MEDIA_ROOT, file_path)
                logger.info(img_full_path)
                # image preview
                image_url = default_storage.url(file_path)
                logger.info(image_url)

                # Preprocess image
                img = tf.keras.utils.load_img(img_full_path, target_size=(256, 256))
                img_array = tf.keras.utils.img_to_array(img)
                img_batch = tf.expand_dims(img_array, axis=0)

                # Prediction
                pred = model.predict(img_batch)
                predicted_index = tf.argmax(pred, axis=1).numpy()[0]
                label = LABELS[predicted_index]
                recyclable_status = "Recyclable" if label in RECYCLABLE else "Non-Recyclable"

                prediction = f"{label.capitalize()} ({recyclable_status})"

            except Exception as e:
                logger.error(f"Prediction error: {e}")
                prediction = f"Error: {e}"

    return render(request, 'predict.html', {
        'form': form,
        'prediction': prediction,
        'image_url': image_url
    })