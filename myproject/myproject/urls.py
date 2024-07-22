from django.contrib import admin
from django.urls import path
from myapp import views  


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('success/', views.success, name='success'),
    path('view_data/', views.view_data, name='view_data'),
    path('data/create/', views.data_create, name='data_create'),
    path('data/<int:id>/update/', views.data_update, name='data_update'),
    path('data/<int:id>/delete/', views.data_delete, name='data_delete'),
    path('data/list/', views.data_list, name='data_list'),  
]
