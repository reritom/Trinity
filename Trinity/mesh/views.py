from django.shortcuts import render
from mesh.meshcore.cortex import *
from mesh.meshcore.spark import *
from mesh.meshcore.relay import *
from mesh.meshcore.propagate import *

# Create your views here.

def test(request):
    print('This is a test')
    return render(request, 'mesh/test.html')

def gogo(request):
    red = propagate()
    return render(request, 'mesh/test.html')
