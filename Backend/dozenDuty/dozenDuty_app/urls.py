from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name='dozenDuty_main'),

    # Groceries
    path('groceries/', views.groceries, name='groceries'),
    path('groceries/add/', views.addGrocery, name='groceries-add'),
    path('groceries/<int:id>/detail/', views.detailGrocery, name='groceries-detail'),
    path('groceries/<int:id>/remove/', views.removeGrocery, name='groceries-remove'),
    path('groceries/<int:id>/update/', views.updateGrocery, name='groceries-update'),
    path('groceries/search/', views.searchGrocery, name='groceries-search_results'),

    # Chores
    path('chores/', views.chores, name='chores'),
    path('chores/add/', views.addChores, name='chores-add'),
    path('chores/<int:id>/detail/', views.detailChores, name='chores-detail'),
    path('chores/<int:id>/remove/', views.removeChores, name='chores-remove'),
    path('chores/<int:id>/update/', views.updateChores, name='chores-update'),
    path('chores/search/', views.searchChores, name='chores-search_results'),
    
    # Members
    path('members/', views.members, name='dozenDuty_members'),
    path('members/add/', views.addMember, name='members-add'),
    path('members/<int:id>/remove/', views.removeMember, name='members-remove'),
    path('members/<int:id>/update/', views.updateMember, name='members-update'),
    path('members/search/', views.searchMember, name='members-search_results'),
]