from client import views
from django.urls import path

urlpatterns = [
    # Auth
    path('login', views.LoginView.as_view()),
    path('register', views.RegistrationView.as_view()),

    # FAQ
    path('faq', views.FAQ.as_view()),

     # FAQ
    path('about', views.About.as_view()),

    # -------- admin urls starts here --------
    # Dashboard
    path('admin/dashboard', views.DashboardView.as_view()),

    # FAQ
    path('admin/manage-faqs', views.FAQList.as_view()),

     # System Information
    path('admin/manage-system-informations', views.SystemInformationList.as_view()),
    
]