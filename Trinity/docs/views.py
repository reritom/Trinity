from django.shortcuts import render

# Create your views here.

def doctest(request):
    return render(request, 'docs/test.html')
