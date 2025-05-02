from django.shortcuts import render
from .forms import UploadImageForm
import numpy as np
import tensorflow as tf
from django.conf import settings
import os
from os.path import join
from tensorflow.keras.preprocessing import image
from loguru import logger
from django.core.files.storage import default_storage




# Create your views here.

ROOT_DIR = settings.BASE_DIR

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



def login_view(request):
    return render(request, 'signin.html')


def register_view(request):
    return render(request, 'signup.html')

def dashboard_view(request):
    return render(request,'dashboard.html')


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