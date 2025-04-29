from django.shortcuts import render

# Create your views here.

def login_view(request):
    return render(request, 'signin.html')


def register_view(request):
    return render(request, 'signup.html')

def dashboard_view(request):
    return render(request,'dashboard.html')