from django.urls import path
from . import views

app_name = 'jasmine'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('export-excel/', views.export_excel_view, name='export_excel'),
]
