from django.urls import path
from task_manager.tasks import views


app_name = 'tasks'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.TaskCreateView.as_view(), name='create'),
    path('<int:pk>/', views.TaskView.as_view(), name='detail'),
    path('<int:pk>/update/', views.TaskUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='delete'),
]
