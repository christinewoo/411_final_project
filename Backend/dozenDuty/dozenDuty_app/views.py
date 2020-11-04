from django.shortcuts import render

def home(request):
    return render(request, 'dozenDuty_app/home.html')

def groceries(request):
    return render(request, 'dozenDuty_app/groceries.html')

def chores(request):
    return render(request, 'dozenDuty_app/chores.html')

def members(request):
    return render(request, 'dozenDuty_app/members.html')