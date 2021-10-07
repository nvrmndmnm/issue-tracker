"""issue_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from webapp import views as webapp_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', webapp_views.ProjectsView.as_view(), name='index'),
    path('projects/', webapp_views.ProjectsView.as_view(), name='projects'),
    path('projects/<int:project_pk>/', webapp_views.ProjectView.as_view(), name='project'),
    path('issues/', webapp_views.IndexView.as_view(), name='issues'),
    path('issues/<int:pk>/', webapp_views.IssueView.as_view(), name='issue'),
    path('issues/create/', webapp_views.CreateIssueView.as_view(), name='create_issue'),
    path('issues/<int:pk>/edit/', webapp_views.EditIssueView.as_view(), name='edit_issue'),
    path('issues/<int:pk>/delete/', webapp_views.DeleteIssueView.as_view(), name='delete_issue'),
    path('filter/', webapp_views.IndexView.as_view(), name='filter'),
    path('search/', webapp_views.SearchView.as_view(), name='search'),
    path('projects/<int:project_pk>/issues/create/', webapp_views.CreateProjectIssueView.as_view(),
         name='create_project_issue'),
    path('projects/create/', webapp_views.CreateProjectView.as_view(), name='create_project')
]
