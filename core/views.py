from django.shortcuts import render

def index(request):
    return render(request, 'base.html')

def register_view(request):
    return render(request, 'register.html')

def user_detail_view(request, user_id):
    return render(request, 'user_detail.html', {'user_id': user_id})