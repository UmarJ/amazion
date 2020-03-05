from django.urls import path
from main import views
from django.conf.urls.static import static
from amazion import settings


urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:product_id>/reviews', views.review,
         name='review'),
    path('product/<pk>/', views.ProductDetailView.as_view(),
         name='product-detail'),
    path('add_product/', views.add_product, name='addproduct'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('account/', views.account_info, name='account-info'),
    path('cart/', views.show_cart, name='show-cart'),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add-to-cart'),
    path('remove_from_cart/<int:product_id>', views.remove_from_cart, name='remove-from-cart'),
    path('checkout', views.checkout, name='checkout'),
    path('transactions', views.transactions, name='transaction-history'),
    path('search/<search_query>', views.search, name='search'),
    path('search/', views.index, name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
