from client import views
from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    #Root
    path('', RedirectView.as_view(url='/login', permanent=False)),
    
    # Auth
    path('login', views.LoginView.as_view()),
    path('register', views.RegistrationView.as_view()),
    
    # FAQ
    path('my-profile', views.UserMyProfile.as_view()),
    path('my-qr', views.UserQRCode.as_view()),
    
    
    # Attendance
    path('attendance-window/<int:pk>', views.AttendanceWindow.as_view()),

    # FAQ
    path('faq', views.FAQ.as_view()),

     # FAQ
    path('about', views.About.as_view()),

    # -------- admin urls starts here --------
    # Dashboard
    path('admin/dashboard', views.DashboardView.as_view()),

    # Department
    path('admin/manage-departments', views.DepartmentList.as_view()),
    
    # User
    path('admin/manage-users', views.UserList.as_view()),
    path('admin/manage-users/create', views.UserCreate.as_view()),
    path('admin/manage-users/<int:pk>', views.UserDetail.as_view()),

    # FAQ
    path('admin/manage-faqs', views.FAQList.as_view()),

    # System Information
    path('admin/manage-system-informations', views.SystemInformationList.as_view()),
    
    # Manage Activities
    path('admin/manage-activities', RedirectView.as_view(url='/admin/manage-activities/groups', permanent=False)),
    path('admin/manage-activities/groups', views.ActivityGroupList.as_view()),
    path('admin/manage-activities/groups/<int:group>', views.ActivityList.as_view()),
    
   
    
]