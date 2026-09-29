from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.home, name='home'),
    path('projects/', views.projects_list, name='projects_list'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('about/', views.about, name='about'),

    
    path('reports/', views.reports_list, name='reports'),
    path('reports/create/', views.create_report, name='create_report'),
    path('reports/<int:pk>/', views.report_detail, name='report_detail'),
    path('reports/<int:pk>/edit/', views.update_report, name='update_report'),
    path('reports/<int:pk>/delete/', views.delete_report, name='delete_report'),
    path('reports/<int:pk>/resolve/', views.resolve_report, name='resolve_report'),
    path('my-reports/', views.my_reports, name='my_reports'),

    
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]