from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

analytics_router = DefaultRouter()
analytics_router.register('analytics', views.AnalyticsView)

urlpatterns = [    
     #Analytics
    path('', include(analytics_router.urls)),
    
    # Auth
    path('login', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('register', views.RegistrationView.as_view()),
    path('change-password', views.ChangePasswordView.as_view()),

    # Profile
    path('profile', views.UserMyProfile.as_view()),
    
    # Notifications 
    path('notifications', views.NotificationList.as_view()),
    path('notifications/mark-as-read-all', views.NotificationMarkReadAll.as_view()),
    path('notifications/<int:pk>/mark-as-read', views.NotificationMarkRead.as_view()),
    path('stream', views.StreamEvent.as_view()),

    # Users
    path('users', views.UserListCreate.as_view()),
    path('users/import', views.UserImport.as_view()),
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
    
    # Reports
    path('report-pdf/', views.ReportPDF.as_view()),
]
