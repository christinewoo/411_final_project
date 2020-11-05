from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Member

def home(request):
    return render(request, 'dozenDuty_app/home.html')

def groceries(request):
	#groceries = GroceryItem.objects.all()
    return render(request, 'dozenDuty_app/groceries.html')
    			  #{'groceries': groceries})

def chores(request):
    return render(request, 'dozenDuty_app/chores.html')

def members(request):
	members = Member.objects.all()
	return render(request, 'dozenDuty_app/members.html', {'members': members})

def addMember(request):
	name = request.POST['memberName']
	new_item = Member(memberName=name)
	new_item.save()
	return HttpResponseRedirect('/members/')

def removeMember(request, id):
	to_remove = Member.objects.get(memberID=id)
	to_remove.delete()
	return HttpResponseRedirect('/members/')