from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.redirect('/dashboard/')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('workflows/', views.workflow_list, name='workflow_list'),
    path('workflows/create/', views.workflow_create, name='workflow_create'),
    path('workflows/<int:pk>/edit/', views.workflow_edit, name='workflow_edit'),
    path('workflows/<int:pk>/delete/', views.workflow_delete, name='workflow_delete'),
    path('workflowsteps/', views.workflowstep_list, name='workflowstep_list'),
    path('workflowsteps/create/', views.workflowstep_create, name='workflowstep_create'),
    path('workflowsteps/<int:pk>/edit/', views.workflowstep_edit, name='workflowstep_edit'),
    path('workflowsteps/<int:pk>/delete/', views.workflowstep_delete, name='workflowstep_delete'),
    path('executions/', views.execution_list, name='execution_list'),
    path('executions/create/', views.execution_create, name='execution_create'),
    path('executions/<int:pk>/edit/', views.execution_edit, name='execution_edit'),
    path('executions/<int:pk>/delete/', views.execution_delete, name='execution_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
