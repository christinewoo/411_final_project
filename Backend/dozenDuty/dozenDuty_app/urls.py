from django.urls import path
from .views import(
    GroceryListView,
    GroceryDetailView,
    GroceryCreateView,
    GroceryUpdateView,
    GroceryDeleteView,
    GrocerySearchResultsView,
)
from . import views


urlpatterns = [
    path('', views.main, name='dozenDuty_main'),
    path('groceries/', GroceryListView.as_view(), name='groceries'),
    path('groceries/<int:pk>/', GroceryDetailView.as_view(), name='groceries-detail'),
    path('groceries/new/', GroceryCreateView.as_view(), name='groceries-create'),
    path('groceries/<int:pk>/update/', GroceryUpdateView.as_view(), name='groceries-update'),
    path('groceries/<int:pk>/delete/', GroceryDeleteView.as_view(), name='groceries-delete'),
    path('groceries/search/', GrocerySearchResultsView.as_view(), name='groceries-search_results'),
    path('chores/', views.chores, name='dozenDuty_chores'),
    path('members/', views.members, name='dozenDuty_members'),
    path('addMember/', views.addMember),
    path('removeMember/<int:id>/', views.removeMember),
]