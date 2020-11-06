from django.shortcuts import render
from django.db.models import Q
from django.db import connection
from django.views.generic import(
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import(
    Grocery,
    Member,
)
from django.http import HttpResponseRedirect

def main(request):
    return render(request, 'dozenDuty_app/main.html')

def groceries(request):
    return render(request, 'dozenDuty_app/groceries.html',{'title':'Groceries'})

class GroceryListView(ListView):
    model = Grocery
    template_name = 'dozenDuty_app/groceries.html'
    context_object_name = 'groceries'
    ordering = ['-purchaseDate']

class GroceryDetailView(DetailView):
    model = Grocery

class GroceryCreateView(CreateView):
    model = Grocery
    fields = ['groceryName', 'ItemType', 'memberName', 'unitPrice', 'quantity']

class GroceryUpdateView(UpdateView):
    model = Grocery
    fields = ['groceryName', 'memberName', 'unitPrice', 'quantity']

class GroceryDeleteView(DeleteView):
    model = Grocery
    success_url = '/'

class GrocerySearchResultsView(ListView):
    model = Grocery
    template_name = 'dozenDuty_app/grocery_search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Grocery.objects.filter(
            Q(groceryName__icontains=query)
        )
        return object_list

def chores(request):
    return render(request, 'dozenDuty_app/chores.html',{'title':'Chores'})

def members(request):
    members = Member.objects.raw('SELECT * FROM dozenDuty_app_member')
    return render(request, 'dozenDuty_app/members.html', {'title':'Members','members': members})

def addMember(request):
    name = request.POST['memberName']
    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO dozenDuty_app_member (memberName) VALUES(%s)',[name])
    return HttpResponseRedirect('/members/')

def removeMember(request, id):
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM dozenDuty_app_member WHERE memberID=%s',[id])
    return HttpResponseRedirect('/members/')

def updateMember(request, id):
    name = request.POST['memberName']
    with connection.cursor() as cursor:
        cursor.execute('UPDATE dozenDuty_app_member SET memberName=%s WHERE memberID=%s',[name,id])
    return HttpResponseRedirect('/members/')

def searchMember(request):
    name = request.GET.get('q')
    search_key = '%' + name + '%'
    with connection.cursor() as cursor:
        cursor.execute("SELECT memberName FROM dozenDuty_app_member WHERE memberName LIKE %s",[search_key])
        members = cursor.fetchall()
    members = list(members)
    for i in range(len(members)):
        members[i] = members[i][0]
    return render(request, 'dozenDuty_app/members_search_results.html', {'title':'Members','members': members, 'name': name})