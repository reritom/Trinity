from django.shortcuts import render
from django.http import JsonResponse
from mesh.meshcore.cortex import *
from mesh.meshcore.spark import *
from mesh.meshcore.relay import *
from mesh.meshcore.propagate import *

# Create your views here.

def home(request):
    print('This is a test')
    return render(request, 'mesh/home.html')

def gogo(request):
    logs = xPingAll(False)

    logs[len(logs)+1] = {'Type':'Device', 'at':'R1Y'}
    return render(request, 'mesh/test.html', {'context':logs})

def examples(request):
    examplesList = []

    '''
    for i in dir(examples):
        item = getattr(examples,i)
        if callable(item):
            examplesList.append(item)
            #item()
            #print("\n")
    '''

    for i in examples.__dict__:
        examplesList.append(i)

    context = {'examples':examplesList}

    return JsonResponse(context)
