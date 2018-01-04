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
    logs = xPingAll(False)

    logs[len(logs)+1] = {'Type':'Device', 'at':'R1Y'}
    return render(request, 'mesh/test.html', {'context':logs})
