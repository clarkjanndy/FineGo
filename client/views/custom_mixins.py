from django.contrib.auth.mixins import UserPassesTestMixin
from django.http.response import HttpResponseRedirect

__all__ = ['AdminRequiredMixin', 'NotAuthenticatedMixin', 'LoginRequiredMixin']

class LoginRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        request = self.request
        return request.user.is_authenticated
    
    def handle_no_permission(self):        
        return  HttpResponseRedirect('/login')

class AdminRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        request = self.request
        return request.user.is_superuser
    
    def handle_no_permission(self):
        request = self.request
        # redirect to login if not authenticated
        if request.user.is_authenticated:
            return  HttpResponseRedirect('/profile')
        
        return  HttpResponseRedirect('/login')
        
class NotAuthenticatedMixin(UserPassesTestMixin):

    def test_func(self):    
        request = self.request
        return not request.user.is_authenticated
    
    def handle_no_permission(self):
        # redirect to dashboard if authenticated
        return  HttpResponseRedirect('admin/dashboard')
    