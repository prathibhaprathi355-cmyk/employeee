from django.urls import path
from . import views

urlpatterns =[
    path('', views.employee_list_view),
    path('<int:employee_id>', views.employee_details_view),


]