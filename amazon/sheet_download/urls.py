from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('templates/', views.templates, name='templates'),
    path('templates/templates_download', views.templates_download, name='templates_download'),
    path('templates/inventory_download', views.inventory_download, name='inventory_download'),
    path('orders/', views.orders, name='orders'),
    path('orders/download', views.download, name='download'),
    path('orders/custom_download', views.custom_download, name='custom_download'),
]
