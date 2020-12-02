from django.shortcuts import render
from django.db import connection
from django.http import HttpResponseRedirect
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
mongodb = client['dozenduty_mongo']

def management_tool():
    with connection.cursor() as cursor:
            cursor.execute("SELECT ItemType, sum(quantity) FROM dozenDuty_app_grocery GROUP BY ItemType ORDER BY ItemType")
            categories = cursor.fetchall()
            cursor.execute("SELECT sum(quantity) FROM dozenDuty_app_grocery")
            total_quantity = cursor.fetchone()[0]

    categories_labels = []
    categories_data = []
    curr_grain_ratio = 0.00
    curr_vegetable_ratio = 0.00
    curr_fruit_ratio = 0.00
    curr_protein_ratio = 0.00
    curr_dairy_ratio = 0.00
    for category in categories:
        if category[0] != 'Other':
            categories_labels.append(category[0])
            categories_data.append(category[1])
            if category[0] == 'Vegetable':
                curr_vegetable_ratio = category[1]/total_quantity
            elif category[0] == 'Protein':
                curr_protein_ratio = category[1]/total_quantity
            elif category[0] == 'Grain':
                curr_grain_ratio = category[1]/total_quantity
            elif category[0] == 'Fruit':
                curr_fruit_ratio = category[1]/total_quantity
            elif category[0] == 'Dairy':
                curr_dairy_ratio = category[1]/total_quantity

    if 'Vegetable' not in categories_labels:
        categories_labels.append('Vegetable')
        categories_data.append(0)
        curr_vegetable_ratio = 0
    if 'Protein' not in categories_labels:
        categories_labels.append('Protein')
        categories_data.append(0)
        curr_protein_ratio = 0
    if 'Grain' not in categories_labels:
        categories_labels.append('Grain')
        categories_data.append(0)
        curr_grain_ratio = 0
    if 'Fruit' not in categories_labels:
        categories_labels.append('Fruit')
        categories_data.append(0)
        curr_fruit_ratio = 0
    if 'Dairy' not in categories_labels:
        categories_labels.append('Dairy')
        categories_data.append(0)
        curr_dairy_ratio = 0




    stan_grain_ratio = 0.27
    stan_vegetable_ratio = 0.38
    stan_fruit_ratio = 0.10
    stan_protein_ratio = 0.20
    stan_dairy_ratio = 0.05

    tooMuch_warning = 'Too Much! Eat less!'
    tooFew_warning = 'Too Few! Eat more!'
    good_warning = 'Doing Good! Keep going!'
    foodType_warning = {}
    if curr_grain_ratio < stan_grain_ratio:
        foodType_warning['Grain'] = tooFew_warning
    elif curr_grain_ratio > 0.5:
        foodType_warning['Grain'] = tooFew_warning
    else:
        foodType_warning['Grain'] = good_warning

    if curr_vegetable_ratio < stan_vegetable_ratio:
        foodType_warning['Vegetable'] = tooFew_warning
    elif curr_grain_ratio > 0.5:
        foodType_warning['Vegetable'] = tooFew_warning
    else:
        foodType_warning['Vegetable'] = good_warning

    if curr_protein_ratio < stan_protein_ratio:
        foodType_warning['Protein'] = tooFew_warning
    elif curr_grain_ratio > 0.5:
        foodType_warning['Protein'] = tooFew_warning
    else:
        foodType_warning['Protein'] = good_warning

    if curr_fruit_ratio < stan_fruit_ratio:
        foodType_warning['Fruit'] = tooFew_warning
    elif curr_grain_ratio > 0.5:
        foodType_warning['Fruit'] = tooFew_warning
    else:
        foodType_warning['Fruit'] = good_warning

    if curr_dairy_ratio < stan_dairy_ratio:
        foodType_warning['Dairy'] = tooFew_warning
    elif curr_grain_ratio > 0.5:
        foodType_warning['Dairy'] = tooFew_warning
    else:
        foodType_warning['Dairy'] = good_warning
    
    return categories_labels, categories_data, foodType_warning

def insertGroceryList(request):
    new_grocery = request.POST['newGrocery']
    mongodb.groceryList.update_one(
            {"listName": 'Current'},
            { 
                "$push": { "groceryNeeded": new_grocery } 
            }
        )
    return HttpResponseRedirect('/')

def resetGroceryList(request):
    mongodb.groceryList.update_one(
            {"listName": 'Current'},
            { 
                "$set": { "listName": 'Past' } 
            }
        )
    mongodb.groceryList.insert_one(
            { 
                "listName": 'Current',
                "groceryNeeded": []
            }
        )
    return HttpResponseRedirect('/')

""" Main Page """
def main(request):
    weights_labels = []
    weights_data = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT m.memberName, sum(c.weight) FROM dozenDuty_app_chore as c LEFT JOIN dozenDuty_app_member as m on c.memberID=m.memberID GROUP BY m.memberID")
        weights = cursor.fetchall()
        cursor.execute("SELECT memberName FROM dozenDuty_app_member")
        members = cursor.fetchall()
    
    for weight in weights:
        weights_labels.append(weight[0])
        weights_data.append(int(weight[1]))

    for member in members:
        if member[0] not in weights_labels:
            weights_labels.append(member[0])
            weights_data.append(0)
    categories_labels, categories_data, foodType_warning = management_tool()
    groceryList = mongodb.groceryList.find_one({"listName":"Current"})['groceryNeeded']
    return render(request, 'dozenDuty_app/main.html', {'categories_labels': categories_labels, 'categories_data': categories_data,'weights_labels': weights_labels, 'weights_data': weights_data, 'foodType_warning':foodType_warning, 'groceryList':groceryList})

""" Groceries Page """
def groceries(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT g.groceryName, m.memberName, g.unitPrice, g.quantity, g.purchaseDate, g.ExpirationDate, g.ItemType, g.ItemUnit, g.groceryID FROM dozenDuty_app_grocery as g LEFT JOIN dozenDuty_app_member as m on g.memberID=m.memberID ORDER BY g.ExpirationDate ASC")
        groceries = cursor.fetchall()
        cursor.execute("SELECT memberID,memberName FROM dozenDuty_app_member")
        members = cursor.fetchall()
    groceries = list(groceries)
    for i in range(len(groceries)):
        groceries[i] += (round(groceries[i][2]*groceries[i][3],2),)
    _, __, foodType_warning = management_tool()
    return render(request, 'dozenDuty_app/groceries.html',{'title':'Groceries','groceries': groceries,'members':members, 'foodType_warning':foodType_warning})

def detailGrocery(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT g.groceryName, m.memberName, g.unitPrice, g.quantity, g.purchaseDate, g.ExpirationDate, g.ItemType, g.ItemUnit, g.groceryID, g.memberID FROM dozenDuty_app_grocery as g LEFT JOIN dozenDuty_app_member as m on g.memberID=m.memberID WHERE groceryID=%s",[id])
        groceries = cursor.fetchone()
        cursor.execute("SELECT memberID,memberName FROM dozenDuty_app_member")
        members = cursor.fetchall()
    total_price = round(groceries[2]*groceries[3],2)
    _, __, foodType_warning = management_tool()
    return render(request, 'dozenDuty_app/grocery_detail.html',{'title':'Groceries','groceries': groceries,'total_price':total_price,'members':members, 'foodType_warning':foodType_warning})

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
        cursor.execute('SELECT count(distinct memberID) FROM dozenDuty_app_member')
        numMember=cursor.fetchone()
        if member_id is not '':
            cursor.execute('UPDATE dozenDuty_app_grocery SET memberID=%s WHERE groceryID=%s',[member_id,id])
        if item_type is not '':
            cursor.execute('UPDATE dozenDuty_app_grocery SET ItemType=%s WHERE groceryID=%s',[item_type,id])
        cursor.execute('UPDATE dozenDuty_app_grocery SET groceryName=%s,unitPrice=%s,quantity=%s,purchaseDate=%s,ExpirationDate=%s,ItemUnit=%s, numMember=%s WHERE groceryID=%s',[grocery_name,unit_price,Quantity,purchase_date,expiration_date,item_unit,numMember[0],id])
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
    _, __, foodType_warning = management_tool()
    return render(request, 'dozenDuty_app/grocery_search_results.html', {'title':'Groceries','groceries': groceries, 'name': name, 'foodType_warning':foodType_warning})


""" Chores Page """
def chores(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT c.choreID, c.name, m.memberName, c.assignDate, c.dueDate, c.status FROM dozenDuty_app_chore as c LEFT JOIN dozenDuty_app_member as m on c.memberID=m.memberID ORDER BY c.dueDate ASC")
        chores = cursor.fetchall()
        cursor.execute("SELECT memberID,memberName FROM dozenDuty_app_member")
        members = cursor.fetchall()
    _, __, foodType_warning = management_tool()
    return render(request, 'dozenDuty_app/chores.html',{'title':'Chores','chores': chores,'members':members, 'foodType_warning':foodType_warning})

def detailChores(request, id):
    _, __, foodType_warning = management_tool()
    with connection.cursor() as cursor:
        cursor.execute("SELECT c.choreID, c.name, m.memberName, c.assignDate, c.dueDate, c.status, c.weight FROM dozenDuty_app_chore as c LEFT JOIN dozenDuty_app_member as m on c.memberID=m.memberID WHERE c.choreID=%s",[id])
        chore = cursor.fetchone()
        cursor.execute("SELECT memberID,memberName FROM dozenDuty_app_member")
        members = cursor.fetchall()
    if (mongodb.choreList.find_one({'choreName':chore[1]})) is None:
        tools = []
    else:
        tools = (mongodb.choreList.find_one({'choreName':chore[1]}))['toolsNeeded']
    return render(request, 'dozenDuty_app/chores_detail.html',{'title':'Chores','chore': chore, 'tools': tools,'members':members, 'foodType_warning':foodType_warning})

def addChores(request):
    assign_date = request.POST['assignDate']
    due_date = request.POST['dueDate']
    member_id = request.POST['memberID']
    chore_name = request.POST['choreName']
    chore_weight = request.POST['weight']
    if mongodb.choreList.find_one({'choreName':chore_name}) is None:
        mongodb.choreList.insert_one(
            {
                "choreName": chore_name, 
                "toolsNeeded": []
            }
        )
    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO dozenDuty_app_chore (memberID,name,assignDate,dueDate,weight) VALUES(%s,%s,%s,%s,%s)',[member_id,chore_name,assign_date,due_date,chore_weight])
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
    toolsNeeded = request.POST['tools']

    with connection.cursor() as cursor:
        if assign_date is not '':
            cursor.execute('UPDATE dozenDuty_app_chore SET assignDate=%s WHERE choreID=%s',[assign_date,id])
        if chore_name is not '':
            cursor.execute('UPDATE dozenDuty_app_chore SET name=%s WHERE choreID=%s',[chore_name,id])
            if mongodb.choreList.find_one({'choreName':chore_name}) is None:
                mongodb.choreList.insert_one(
                    {
                        "choreName": chore_name, 
                        "toolsNeeded": []
                    }
                )
        if member_id is not '':
            cursor.execute('UPDATE dozenDuty_app_chore SET memberID=%s WHERE choreID=%s',[member_id,id])
        if due_date is not '':
            cursor.execute('UPDATE dozenDuty_app_chore SET dueDate=%s WHERE choreID=%s',[due_date,id])
        if cur_status is not '':
            cursor.execute('UPDATE dozenDuty_app_chore SET status=%s WHERE choreID=%s',[cur_status,id])
        if toolsNeeded is not '':
            tools_needed = toolsNeeded.split("; ")
            mongodb.choreList.update_one(
                {"choreName": chore_name},
                { 
                    "$set": { "toolsNeeded": tools_needed } 
                }
            )
    chore_detail_url = '/chores/' + str(id) + '/detail/'
    return HttpResponseRedirect(chore_detail_url)

def searchChores(request):
    _, __, foodType_warning = management_tool()
    name = request.GET.get('q')
    search_key = '%' + name + '%'
    with connection.cursor() as cursor:
        cursor.execute("SELECT c.choreID, c.name, m.memberName, c.assignDate, c.dueDate, c.status FROM dozenDuty_app_chore as c LEFT JOIN dozenDuty_app_member as m on c.memberID=m.memberID WHERE c.name LIKE %s or m.memberName LIKE %s or c.status LIKE %sORDER BY c.dueDate ASC",[search_key,search_key,search_key])
        chores = cursor.fetchall()
    return render(request, 'dozenDuty_app/chores_search_results.html', {'title':'Chores','chores': chores, 'name': name, 'foodType_warning':foodType_warning})


""" Members Page """
def members(request):
    _, __, foodType_warning = management_tool()
    with connection.cursor() as cursor:
        cursor.execute("SELECT mo.borrowerID, m.memberName, SUM(mo.amount) FROM dozenDuty_app_member m JOIN dozenDuty_app_money mo ON m.memberID=mo.borrowerID GROUP BY mo.borrowerID, m.memberName ORDER BY m.memberID") 
        temp = cursor.fetchall()
        cursor.execute("SELECT * FROM dozenDuty_app_member") 
        one_member = cursor.fetchone()
    members = []
    if len(temp) == 0 and one_member is not None:
        members.append((one_member[0], one_member[1], 0.00))
    else:
        members = list(temp)
        for i in range(len(temp)):
            if members[i][2] == 0:
                members[i] = (members[i][0], members[i][1], round(members[i][2], 2))
            else:
                members[i] = (members[i][0], members[i][1], round(members[i][2]*(-1), 2))
    return render(request, 'dozenDuty_app/members.html', {'title':'Members','members': members, 'foodType_warning':foodType_warning})

def detailMember(request, id):
    _, __, foodType_warning = management_tool()
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
    return render(request, 'dozenDuty_app/members_detail.html',{'title':'Members','member': cur_member, 'debts': debts, 'foodType_warning':foodType_warning})

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
    _, __, foodType_warning = management_tool()
    name = request.GET.get('q')
    search_key = '%' + name + '%'
    with connection.cursor() as cursor:
        cursor.execute(" SELECT DISTINCT mo.borrowerID, m.memberName, SUM(mo.amount) FROM dozenDuty_app_member m JOIN dozenDuty_app_money mo ON m.memberID=mo.borrowerID WHERE memberName LIKE %s GROUP BY mo.borrowerID, m.memberName",[search_key])
        temp = cursor.fetchall()
        cursor.execute("SELECT * FROM dozenDuty_app_member WHERE memberName LIKE %s",[search_key]) 
        one_member = cursor.fetchone()
    members = []
    if len(temp) == 0 and one_member is not None:
        members.append((one_member[0], one_member[1], 0.00))
    else:
        members = list(temp)
        for i in range(len(temp)):
            if members[i][2] == 0:
                members[i] = (members[i][0], members[i][1], round(members[i][2], 2))
            else:
                members[i] = (members[i][0], members[i][1], round(members[i][2]*(-1), 2))
    return render(request, 'dozenDuty_app/members_search_results.html', {'title':'Members','members': members, 'name': name, 'foodType_warning':foodType_warning})
