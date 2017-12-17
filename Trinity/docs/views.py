from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# Create your views here.

def mainDocs(request):
    return render(request, 'docs/test.html')

def exampleDocs(request):
    examples = getExampleDocstrings()
    # Parse docstring into dict of titles and content
    return JsonResponse(examples)

def getExampleDocstrings():
    docDict = dict()

    import mesh.meshcore.propagate as examples
    for i in dir(examples):
        item = getattr(examples,i)
        if callable(item):
            docDict[item.__name__] = item.__doc__

    return docDict
