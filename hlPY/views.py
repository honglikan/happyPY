from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'home.html',locals())


def login(request):
    pass

def register(request):
    pass

def ide(request):
    return render(request,'ide.html',locals())