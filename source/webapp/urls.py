from django.urls import path
from webapp import views as webapp_views

app_name = 'webapp'

urlpatterns = [
    path('', webapp_views.IndexView.as_view(), name='index'),
    path('projects/', webapp_views.ProjectsView.as_view(), name='projects'),
    path('projects/<int:project_pk>/', webapp_views.ProjectView.as_view(), name='project'),
    path('projects/<int:project_pk>/update_users/', webapp_views.UpdateProjectUsersView.as_view(),
         name='update_project_users'),
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
