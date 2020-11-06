from django.shortcuts import render
from django.db.models import Q
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
    members = Member.objects.all()
    return render(request, 'dozenDuty_app/members.html', {'title':'Members','members': members})

def addMember(request):
	name = request.POST['memberName']
	new_item = Member(memberName=name)
	new_item.save()
	return HttpResponseRedirect('/members/')

def removeMember(request, id):
	to_remove = Member.objects.get(memberID=id)
	to_remove.delete()
	return HttpResponseRedirect('/members/')