from django.shortcuts import render
from django.db import connection
from django.http import HttpResponseRedirect

""" Main Page """
def main(request):
    return render(request, 'dozenDuty_app/main.html')

""" Groceries Page """
def groceries(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT g.groceryName, m.memberName, g.unitPrice, g.quantity, g.purchaseDate, g.ExpirationDate, g.ItemType, g.ItemUnit, g.groceryID FROM dozenDuty_app_grocery as g LEFT JOIN dozenDuty_app_member as m on g.memberID=m.memberID ORDER BY g.ExpirationDate ASC")
        groceries = cursor.fetchall()
    groceries = list(groceries)
    for i in range(len(groceries)):
        groceries[i] += (round(groceries[i][2]*groceries[i][3],2),)
    return render(request, 'dozenDuty_app/groceries.html',{'title':'Groceries','groceries': groceries})

def detailGrocery(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT g.groceryName, m.memberName, g.unitPrice, g.quantity, g.purchaseDate, g.ExpirationDate, g.ItemType, g.ItemUnit, g.groceryID, g.memberID FROM dozenDuty_app_grocery as g LEFT JOIN dozenDuty_app_member as m on g.memberID=m.memberID WHERE groceryID=%s",[id])
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
        cursor.execute('INSERT INTO dozenDuty_app_grocery (groceryName,memberID,unitPrice,quantity,purchaseDate,ExpirationDate,ItemType,ItemUnit,numMember) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,(SELECT count(distinct memberID) FROM dozenDuty_app_member))',[grocery_name,member_id,unit_price,Quantity,purchase_date,expiration_date,item_type,item_unit])
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
    expiration_date = request.POST['ExpirationDate']
    item_type = request.POST['ItemType']
    item_unit = request.POST['ItemUnit']
    with connection.cursor() as cursor:
        cursor.execute('SELECT count(distinct memberID) FROM dozenDuty_app_member');
        numMember=cursor.fetchone();
        cursor.execute('UPDATE dozenDuty_app_grocery SET groceryName=%s,memberID=%s,unitPrice=%s,quantity=%s,purchaseDate=%s,ExpirationDate=%s,ItemType=%s,ItemUnit=%s, numMember=%s WHERE groceryID=%s',[grocery_name,member_id,unit_price,Quantity,purchase_date,expiration_date,item_type,item_unit,numMember[0],id])
    grocery_detail_url = '/groceries/' + str(id) + '/detail/'
    return HttpResponseRedirect(grocery_detail_url)

def searchGrocery(request):
    name = request.GET.get('q')
    search_key = '%' + name + '%'
    with connection.cursor() as cursor:
        cursor.execute(" SELECT g.groceryName, m.memberName, g.unitPrice, g.quantity, g.purchaseDate, g.ExpirationDate, g.ItemType, g.ItemUnit, g.groceryID FROM dozenDuty_app_grocery as g LEFT JOIN dozenDuty_app_member as m on g.memberID=m.memberID WHERE g.groceryName LIKE %s or m.memberName LIKE %s or g.ItemType LIKE %s ORDER BY g.ExpirationDate ASC",[search_key,search_key,search_key])
        groceries = cursor.fetchall()
    groceries = list(groceries)
    for i in range(len(groceries)):
        groceries[i] += (round(groceries[i][2]*groceries[i][3],2),)
    return render(request, 'dozenDuty_app/grocery_search_results.html', {'title':'Groceries','groceries': groceries, 'name': name})


""" Chores Page """
def chores(request):
    # return render(request, 'dozenDuty_app/chores.html',{'title':'Chores'})
    with connection.cursor() as cursor:
        cursor.execute("SELECT c.choreID, c.name, m.memberName, c.assignDate, c.dueDate, c.status FROM dozenDuty_app_chore as c LEFT JOIN dozenDuty_app_member as m on c.memberID=m.memberID ORDER BY c.dueDate ASC")
        chores = cursor.fetchall()
    return render(request, 'dozenDuty_app/chores.html',{'title':'Chores','chores': chores})

def detailChores(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT c.choreID, c.name, m.memberName, c.assignDate, c.dueDate, c.status FROM dozenDuty_app_chore as c LEFT JOIN dozenDuty_app_member as m on c.memberID=m.memberID WHERE c.choreID=%s",[id])
        chore = cursor.fetchone()
    return render(request, 'dozenDuty_app/chores_detail.html',{'title':'Chores','chore': chore})

def addChores(request):
    assign_date = request.POST['assignDate']
    due_date = request.POST['dueDate']
    member_id = request.POST['memberID']
    chore_name = request.POST['choreName']
    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO dozenDuty_app_chore (memberID,name,assignDate,dueDate) VALUES(%s,%s,%s,%s)',[member_id,chore_name,assign_date,due_date])
    return HttpResponseRedirect('/chores/')

def removeChores(request, id):
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM dozenDuty_app_chore WHERE choreID=%s',[id])
    return HttpResponseRedirect('/chores/')

def updateChores(request, id):
    assign_date = request.POST['assignDate']
    chore_name = request.POST['choreName']
    member_id = request.POST['memberID']
    due_date = request.POST['dueDate']
    cur_status = request.POST['status']
    with connection.cursor() as cursor:
        if assign_date is not '':
            cursor.execute('UPDATE dozenDuty_app_chore SET assignDate=%s WHERE choreID=%s',[assign_date,id])
        if chore_name is not '':
            cursor.execute('UPDATE dozenDuty_app_chore SET name=%s WHERE choreID=%s',[chore_name,id])
        if member_id is not '':
            cursor.execute('UPDATE dozenDuty_app_chore SET memberID=%s WHERE choreID=%s',[member_id,id])
        if due_date is not '':
            cursor.execute('UPDATE dozenDuty_app_chore SET dueDate=%s WHERE choreID=%s',[due_date,id])
        if cur_status is not '':
            cursor.execute('UPDATE dozenDuty_app_chore SET status=%s WHERE choreID=%s',[cur_status,id])
    chore_detail_url = '/chores/' + str(id) + '/detail/'
    return HttpResponseRedirect(chore_detail_url)

def searchChores(request):
    name = request.GET.get('q')
    search_key = '%' + name + '%'
    with connection.cursor() as cursor:
        cursor.execute("SELECT c.choreID, c.name, m.memberName, c.assignDate, c.dueDate, c.status FROM dozenDuty_app_chore as c LEFT JOIN dozenDuty_app_member as m on c.memberID=m.memberID WHERE c.name LIKE %s or m.memberName LIKE %s ORDER BY c.dueDate ASC",[search_key,search_key])
        chores = cursor.fetchall()
    return render(request, 'dozenDuty_app/chores_search_results.html', {'title':'Chores','chores': chores, 'name': name})


""" Members Page """
def members(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT mo.borrowerID, m.memberName, SUM(mo.amount) FROM dozenDuty_app_member m JOIN dozenDuty_app_money mo ON m.memberID=mo.borrowerID GROUP BY mo.borrowerID, m.memberName") 
        temp = cursor.fetchall()
    members = list(temp)
    for i in range(len(members)):
        if members[i][2] == 0:
            members[i] = (members[i][0], members[i][1], round(members[i][2], 2))
        else:
            members[i] = (members[i][0], members[i][1], round(members[i][2]*(-1), 2))
    return render(request, 'dozenDuty_app/members.html', {'title':'Members','members': members})

def detailMember(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT m.memberId, m.memberName, mo.moneyID, mo.borrowerID, mo.lenderID, mo.amount FROM dozenDuty_app_member as m LEFT JOIN dozenDuty_app_money as mo on m.memberID=mo.borrowerID WHERE m.memberID=%s",[id])
        cur_member = cursor.fetchone()
        cursor.execute("SELECT DISTINCT * FROM dozenDuty_app_member")
        lookup = cursor.fetchall()
        cursor.execute("SELECT DISTINCT * FROM dozenDuty_app_money mo WHERE mo.borrowerID=%s",[id])
        all_debts = cursor.fetchall()
    debts = list(all_debts)
    lookup = list(lookup)
    for i in range(len(debts)):
        for j in range(len(lookup)):
            if (all_debts[i][1] is lookup[j][0]):
                debts[i] = (all_debts[i][0], lookup[j][1], all_debts[i][2], round(all_debts[i][3],2))
        for k in range(len(lookup)):
            if (all_debts[i][2] is lookup[k][0]):
                debts[i] = (all_debts[i][0], debts[i][1], lookup[k][1], round(all_debts[i][3],2)) 
    return render(request, 'dozenDuty_app/members_detail.html',{'title':'Members','member': cur_member, 'debts': debts})

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
        cursor.execute(" SELECT DISTINCT mo.borrowerID, m.memberName, SUM(mo.amount) FROM dozenDuty_app_member m JOIN dozenDuty_app_money mo ON m.memberID=mo.borrowerID WHERE memberName LIKE %s GROUP BY mo.borrowerID, m.memberName",[search_key])
        members = cursor.fetchall()
    members = list(members)
    for i in range(len(members)):
        if members[i][2] == 0:
            members[i] = (members[i][0], members[i][1], round(members[i][2], 2))
        else:
            members[i] = (members[i][0], members[i][1], round(members[i][2]*(-1), 2))
    return render(request, 'dozenDuty_app/members_search_results.html', {'title':'Members','members': members, 'name': name})
