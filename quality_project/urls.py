from django.contrib import admin
from django.urls import path, include
from nomina import views
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', views.login_view, name='login'),  
    path('dashboard/', views.dashboard, name='dashboard'),  
    path('nomina/', include('nomina.urls')),  
     path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('', views.inicio, name='home'),
]   
