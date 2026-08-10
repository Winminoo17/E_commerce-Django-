from django.urls import path # type: ignore
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('registor/', views.registor_user, name='registor'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_password/', views.update_password, name='update_password'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:foo>', views.category, name='category'),
    path('category_summary/<str:foo>', views.category_summary, name='category_summary'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('search/', views.search, name='search'),
]