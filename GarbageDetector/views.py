from django.shortcuts import render
from .forms import UploadImageForm
import numpy as np
import tensorflow as tf
from django.conf import settings
import os
from os.path import join
from tensorflow.keras.preprocessing import image



# Create your views here.

ROOT_DIR = settings.BASE_DIR

def login_view(request):
    return render(request, 'signin.html')


def register_view(request):
    return render(request, 'signup.html')

def dashboard_view(request):
    return render(request,'dashboard.html')


model_path = os.path.join(settings.BASE_DIR, 'AI_model/garbage_model.keras')
model = tf.keras.models.load_model(model_path)

def garbage_predict(request):

    prediction = None
    
    if request.method == "POST":
        form = UploadImageForm(request.POST,request.FILES)
        if form.is_valid():

            try:
                img_file = request.FILES['image']
                file_path = default_storage.sabe('temp/'+img_file.name,img_file)

                img_path = os.path.join(default_storage.location,file_path)

                img = tf.keras.utils.load_img(img_path,target_size=(256,256))
                img_arr = tf.keras.utils.array_to_img(img)
                img_bat = tf.expand_dims(img_arr,0)

                pred = model.predict(img_bat)
                predicted_class = tf.argmax(pred,axis=1).numpy()[0]

                prediction = predicted_class

            except exception as e:
                prediction = f"Error {str(e)}"

    else:
        form = UploadImageForm()


    return render(request,'predict.html',{'form':form,'prediction':prediction})

