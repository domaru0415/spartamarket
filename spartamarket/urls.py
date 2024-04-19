
from django.contrib import admin
from django.urls import path
from accounts import views as accounts_views
from products import views as products_views
from mainpage import views as main_views
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', accounts_views.signup, name='signup'),
    path('signin/', accounts_views.signin, name='signin'),
    path('signout/', accounts_views.signout, name='signout'),
    path('mainpage/', main_views.home, name='home'),
    path('profile/<str:username>/', accounts_views.profile, name='profile'),
    path('follow/<str:username>/', accounts_views.follow, name='follow'),

    path('', products_views.ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', products_views.ProductDetailView.as_view(), name='product_detail'),
    path('create/', products_views.ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/update/', products_views.ProductUpdateView.as_view(), name='product_update'),
    path('<int:pk>/delete/', products_views.ProductDeleteView.as_view(), name='product_delete'),
    path('<int:pk>/like/', products_views.like_product, name='product_like'),
]