
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from . import views
from .views import FolderManager, MainInterfaceView

urlpatterns = [
    # auth
    path('', views.login_view, name='home'),
    path('register/', views.Register.as_view(), name='register'),
    path('logout/', views.logout_view, name='logout'),

    # foldermanager
    path('create_dir', FolderManager.as_view(), name="create_dir"),
    path('delete_dir', FolderManager.as_view(), name="delete_dir"),
    # path('rename_dir', FolderManager.as_view(), name='rename_dir'),

    # filemanager
    path('upload', views.FileManager.as_view(), name="upload"),
    path('download/<str:data_id>', views.download, name="download"),
    path('delete/<str:data_id>', views.delete, name='delete'),

    # action logs
    path('delete_logs/<path:webpath>', views.delete_logs, name='delete'),

    # front-end
    path('main/', MainInterfaceView.as_view(), name='main'),
    path('main/<path:dir_webpath>/', MainInterfaceView.as_view(), name='submain'),
]
