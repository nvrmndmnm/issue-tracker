from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import RegisterView, UserListView, UserDetailView, UserUpdateView

app_name = 'accounts'

urlpatterns = [
    path('', UserListView.as_view(), name='profiles'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', RegisterView.as_view(), name='create'),
    path('<int:pk>/', UserDetailView.as_view(), name='profile'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='update')
]
