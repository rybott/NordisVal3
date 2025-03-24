from django.shortcuts import render,redirect

def main(request):
    context = {}
    return render(request, 'home.html', context)

def contact(request):
    context = {}
    return render(request, 'contact.html', context)
