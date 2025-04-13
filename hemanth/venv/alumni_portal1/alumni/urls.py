from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('register/', views.register_alumni, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:id>/register/', views.event_register, name='event_register'),
    path('alumni/', views.alumni_list, name='alumni_list'),
    path('announcements/', views.announcements, name='announcements'),
    path('admin-board/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/events/add/', views.add_event, name='add_event'), 

    # 🔄 Updated to avoid conflict
    path('dashboard/announcement/new/', views.create_announcement, name='create_announcement'),
]
