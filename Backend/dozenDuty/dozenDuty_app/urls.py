from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name='dozenDuty_main'),

    path('groceries/', views.groceries, name='groceries'),
    path('groceries/add/', views.addGrocery, name='groceries-add'),
    path('groceries/<int:id>/detail/', views.detailGrocery, name='groceries-detail'),
    path('groceries/<int:id>/remove/', views.removeGrocery, name='groceries-remove'),
    path('groceries/<int:id>/update/', views.updateGrocery, name='groceries-update'),
    path('groceries/search/', views.searchGrocery, name='groceries-search_results'),

    path('chores/', views.chores, name='dozenDuty_chores'),

    path('members/', views.members, name='dozenDuty_members'),
    path('members/add/', views.addMember, name='members-add'),
    path('members/<int:id>/remove/', views.removeMember, name='members-remove'),
    path('members/<int:id>/update/', views.updateMember, name='members-update'),
    path('members/search/', views.searchMember, name='members-search_results'),
]