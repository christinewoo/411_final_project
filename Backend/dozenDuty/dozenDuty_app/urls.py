from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='dozenDuty_home'),
    path('groceries/', views.groceries, name='dozenDuty_groceries'),
    path('chores/', views.chores, name='dozenDuty_chores'),
    path('members/', views.members, name='dozenDuty_members'),
    path('addMember/', views.addMember),
    path('removeMember/<int:id>/', views.removeMember),
]