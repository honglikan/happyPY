from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'home.html',locals())


def login(request):
    pass

def register(request):
    pass