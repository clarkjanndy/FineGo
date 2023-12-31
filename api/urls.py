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

]
