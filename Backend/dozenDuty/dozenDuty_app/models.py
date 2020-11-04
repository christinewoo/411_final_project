from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Member(models.Model):
    memberID = models.AutoField(primary_key=True) 
    memberName = models.CharField(max_length=100)
    
    def __str__(self):
        return self.memberName
 
 
class Home(models.Model):
    homeID = models.AutoField(primary_key=True) 
    memberID = models.ForeignKey(Member, on_delete=models.CASCADE)
    homeName = models.CharField(max_length=30)
    class Meta:
        unique_together = (('homeID', 'memberID'),)
    
    def __str__(self):
        return self.homeName
 
class Grocery(models.Model):
    groceryID = models.AutoField(primary_key=True) 
    groceryName = models.CharField(max_length=50)
    memberID = models.ForeignKey(Member, on_delete=models.CASCADE)
    unitPrice =  models.FloatField()
    quantity = models.IntegerField()
    purchaseDate = models.DateField()
    ExpirationDate = models.DateField()
    ItemType = models.CharField(max_length=30)

    def __str__(self):
        return self.groceryName
 
 
class Chore(models.Model):
    choreID = models.AutoField(primary_key=True)
    choreName = models.CharField(max_length=30) 
    memberID = models.ForeignKey(Member, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    dueDate = models.DateField()
    status = models.CharField(max_length=5)
    steps = models.IntegerField(default=1)
    	
    def __str__(self):
	    return self.choreName
 
class Contain(models.Model):
    memberID = models.ForeignKey(Member, on_delete=models.CASCADE, primary_key=True)
    homeID = models.ForeignKey(Home, on_delete=models.CASCADE)
    class Meta:
        unique_together = (('memberID', 'homeID'),)
    
    def __str__(self):
	    return 'Member: ' +  str(self.memberID) + ' in ' + 'Home: ' +  str(self.homeID)
 
 
class Shop(models.Model):
    groceryID = models.ForeignKey(Grocery, on_delete=models.CASCADE, primary_key=True)
    homeID = models.ForeignKey(Home, on_delete=models.CASCADE)
    class Meta:
        unique_together = (('groceryID', 'homeID'),)
	
    def __str__(self):
	    return 'Grocery: ' +  str(self.groceryID) + ' shopped by ' + 'Home: ' +  str(self.homeID)
 
 
 
class Does(models.Model):
    choreID = models.ForeignKey(Chore, on_delete=models.CASCADE, primary_key=True)
    homeID = models.ForeignKey(Home, on_delete=models.CASCADE)
    class Meta:
        unique_together = (('choreID', 'homeID'),)
	
    def __str__(self):
	    return 'Chore: ' +  str(self.choreID) + ' done by ' + 'Home: ' +  str(self.homeID)