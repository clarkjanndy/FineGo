from django.urls import path
from api import views

urlpatterns = [
    # Auth
    path('login', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('register', views.RegistrationView.as_view()),
    path('change-password', views.ChangePasswordView.as_view()),

    # Profile
    path('profile', views.UserMyProfile.as_view()),

    # Users
    path('users', views.UserListCreate.as_view()),
    path('users/<int:pk>', views.UserById.as_view()),
    path('users/<int:pk>/activate-or-deactivate', views.UserActivateDeactivate.as_view()),

    # Department
    path('departments', views.DepartmentListCreate.as_view()),
    path('departments/<int:pk>', views.DepartmentById.as_view()),
   
    # FAQ
    path('faqs', views.FAQListCreate.as_view()),
    path('faqs/<int:pk>', views.FAQById.as_view()),

    # System Information
    path('system-informations', views.SystemInformationListCreate.as_view()),
    path('system-informations/<int:pk>', views.SystemInformationById.as_view()),
    
    # Activity
    path('activity-groups', views.ActivityGroupListCreate.as_view()),
    path('activity-groups/<int:pk>', views.ActivityGroupById.as_view()),
    path('activity-groups/<int:group>/activities', views.ActivityListCreate.as_view()),
    path('activity-groups/<int:group>/activities/<int:pk>', views.ActivityById.as_view()),
    path('activity-groups/<int:group>/activities/<int:pk>/close', views.ActivityClose.as_view()),
    path('activity-groups/<int:group>/activities/<int:pk>/open', views.ActivityOpen.as_view()),
    
    # Attendance
    path('attendance', views.AttendanceCreate.as_view()),
    
    # Fine
    path('fines/<int:pk>', views.FineById.as_view()),

]
