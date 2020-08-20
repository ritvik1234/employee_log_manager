from django.urls import path
from . import views

urlpatterns = [
  path('',views.home, name='home'),
  path('log', views.log, name= 'log'),
  path('logout', views.logout_view, name= 'logout'),
  path('checkin', views.checkin, name = 'checkin'),
  path('aftercheckin', views.aftercheckin, name = 'checkin'),
  path('aftercheckout', views.aftercheckout, name = 'checkout'),
  path('afterbreak', views.afterbreak, name = 'break'),
  path('create_user', views.create_user, name = 'create_user'),
  path('checkout', views.checkout, name = 'checkout'),
  path('update', views.update, name = 'update'),
  path('admin_create', views.admin_create, name = 'admin_create'),
  path('admin_update', views.admin_update, name = 'admin_update'),
  path('admin_delete', views.admin_delete, name = 'admin_delete'),
  path('delete', views.delete, name = 'delete'),
  path('update_details', views.update_details, name = 'update_details'),
  path('break', views.breakk, name = 'break'),
  path('salary', views.salary, name = 'salary'),
  path('time',views.time, name = 'time'),
  path('update_success',views.update_success, name = 'update_success'),
  path('register',views.register, name = 'register'),
  path('manpower',views.manpower,name = 'manpower'),
  path('employees',views.employees, name = 'employees')
  ]
