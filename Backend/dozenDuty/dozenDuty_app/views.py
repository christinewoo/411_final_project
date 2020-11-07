from django.shortcuts import render
from django.db import connection
from .models import(
    Grocery,
    Member,
)
from django.http import HttpResponseRedirect

""" Main Page """
def main(request):
    return render(request, 'dozenDuty_app/main.html')

""" Groceries Page """
def groceries(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT g.groceryName, m.memberName, g.unitPrice, g.quantity, g.purchaseDate, g.ExpirationDate, g.ItemType, g.ItemUnit, g.groceryID FROM dozenDuty_app_grocery as g LEFT JOIN dozenDuty_app_member as m on g.memberID=m.memberID ")
        groceries = cursor.fetchall()
    groceries = list(groceries)
    for i in range(len(groceries)):
        groceries[i] += (round(groceries[i][2]*groceries[i][3],2),)
    return render(request, 'dozenDuty_app/groceries.html',{'title':'Groceries','groceries': groceries})

def detailGrocery(request, id):
    print(id)
    with connection.cursor() as cursor:
        cursor.execute("SELECT g.groceryName, m.memberName, g.unitPrice, g.quantity, g.purchaseDate, g.ExpirationDate, g.ItemType, g.ItemUnit, g.groceryID FROM dozenDuty_app_grocery as g LEFT JOIN dozenDuty_app_member as m on g.memberID=m.memberID WHERE groceryID=%s",[id])
        groceries = cursor.fetchone()
    total_price = round(groceries[2]*groceries[3],2)
    return render(request, 'dozenDuty_app/grocery_detail.html',{'title':'Groceries','groceries': groceries,'total_price':total_price})

def addGrocery(request):
    grocery_name = request.POST['groceryName']
    member_id = request.POST['memberID']
    unit_price = request.POST['unitPrice']
    Quantity = request.POST['quantity']
    purchase_date = request.POST['purchaseDate']
    expiration_date = request.POST['ExpirationDate']
    item_type = request.POST['ItemType']
    item_unit = request.POST['ItemUnit']
    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO dozenDuty_app_grocery (groceryName,memberID,unitPrice,quantity,purchaseDate,ExpirationDate,ItemType,ItemUnit) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',[grocery_name,member_id,unit_price,Quantity,purchase_date,expiration_date,item_type,item_unit])
    return HttpResponseRedirect('/groceries/')

def removeGrocery(request, id):
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM dozenDuty_app_grocery WHERE groceryID=%s',[id])
    return HttpResponseRedirect('/groceries/')

def updateGrocery(request, id):
    grocery_name = request.POST['groceryName']
    member_id = request.POST['memberID']
    unit_price = request.POST['unitPrice']
    Quantity = request.POST['quantity']
    purchase_date = request.POST['purchaseDate']
    expriation_date = request.POST['ExpirationDate']
    item_type = request.POST['ItemType']
    item_unit = request.POST['ItemUnit']
    with connection.cursor() as cursor:
        cursor.execute('UPDATE dozenDuty_app_grocery SET groceryName=%s,memberID=%s,unitPrice=%s,quantity=%s,purchaseDate=%s,ExpirationDate=%s,ItemType=%s,ItemUnit=%s WHERE groceryID=%s',[grocery_name,member_id,unit_price,Quantity,purchase_date,expiration_date,item_type,item_unit,id])
    return HttpResponseRedirect('/groceries/id/')

def searchGrocery(request):
    name = request.GET.get('q')
    search_key = '%' + name + '%'
    with connection.cursor() as cursor:
        cursor.execute(" SELECT g.groceryName, m.memberName, g.unitPrice, g.quantity, g.purchaseDate, g.ExpirationDate, g.ItemType, g.ItemUnit, g.groceryID FROM dozenDuty_app_grocery as g LEFT JOIN dozenDuty_app_member as m on g.memberID=m.memberID WHERE g.groceryName LIKE %s or m.memberName LIKE %s",[search_key,search_key])
        groceries = cursor.fetchall()
    groceries = list(groceries)
    for i in range(len(groceries)):
        groceries[i] += (round(groceries[i][2]*groceries[i][3],2),)
    return render(request, 'dozenDuty_app/grocery_search_results.html', {'title':'Groceries','groceries': groceries, 'name': name})


""" Chores Page """
def chores(request):
    return render(request, 'dozenDuty_app/chores.html',{'title':'Chores'})

""" Members Page """
def members(request):
    with connection.cursor() as cursor:
        cursor.execute(" SELECT * FROM dozenDuty_app_member ")
        members = cursor.fetchall()
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
        cursor.execute(" SELECT * FROM dozenDuty_app_member WHERE memberName LIKE %s ",[search_key])
        members = cursor.fetchall()
    return render(request, 'dozenDuty_app/members_search_results.html', {'title':'Members','members': members, 'name': name})