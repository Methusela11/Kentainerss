from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from shop import views


urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart_page'),
    path('cartslide', views.cart_items_views, name='cartslide'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('water-tanks/', views.water_tank_storage, name='water_tank_storage'),
    path('sanitation/', views.sanitation_storage, name='sanitation'),
    path('agriculture/', views.agriculture, name='agriculture'),
    path('material-handling/', views.material_handling, name='material_handling'),
    path('water_supply_and_accessories/', views.water_supply_and_accessories, name='water_supply_and_accessories'),
    path('special_products_and_others/', views.special_products_and_others, name='special_products_and_others'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)