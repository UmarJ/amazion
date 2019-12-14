from django.urls import path
from main import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<product_id_slug>/', views.productDetails),
    path('add_product/', views.add_product, name='addproduct'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
]
