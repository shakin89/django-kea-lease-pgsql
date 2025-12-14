from django.urls import path
from . import views

urlpatterns = [
    path('leases/', views.lease4_list, name='lease4_list_url'),
    path('leases/delete/', views.lease4_delete, name='lease4_delete_url'),
]
