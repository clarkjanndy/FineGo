from django.db.models import Q, Sum, F, Case, When, Value, CharField
from django.views.generic import ListView

from api.models import Fine, User

from .custom_mixins import AdminRequiredMixin, LoginRequiredMixin

__all__ = ['UserFines', 'FineList', 'FinesByUser'] 

class UserFines(LoginRequiredMixin, ListView):
    template_name = 'client/my-fines.html'
    queryset = Fine.objects.all()
    paginate_by = 10
    ordering = ('-modified_at', )
    
    def fines_aggregate(self):
        total_fines = self.queryset.filter(user = self.request.user).\
            exclude(status = 'removed').\
            aggregate(amount=Sum('amount'))['amount']
            
        paid_fines = self.queryset.filter(user = self.request.user, status='paid').\
            aggregate(amount=Sum('amount'))['amount']
                        
        unpaid_fines = self.queryset.filter(user = self.request.user, status='unpaid').\
            aggregate(amount=Sum('amount'))['amount']
            
        return {
            "total_fines": total_fines,
            "paid_fines": paid_fines,
            "unpaid_fines": unpaid_fines
        }
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'current_page': 'my-fines'})
        context.update({'fines_aggregate': self.fines_aggregate()})
        return context

    def get_queryset(self):
        # Get current request
        request = self.request
        queryset = super().get_queryset()
        queryset = queryset.filter(user = request.user)
        
        # Get query params
        params = request.GET

        # Get the desired page size from the request's GET parameter
        page_size = params.get('page_size', self.paginate_by)
        # Set the paginate_by attribute to the desired page size
        self.paginate_by = page_size
        
        # Filter results
        if 'q' in params:
            queryset = queryset.filter(
                Q(activity__name__icontains = params['q']) |
                Q(activity__group__name__icontains = params['q'])
            )
        return queryset
    
class FineList(AdminRequiredMixin, ListView):
    template_name = 'client/admin/fine/list.html'
    queryset = Fine.objects.all()
    paginate_by = 10
    ordering = ('-modified_at', )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'current_page': 'manage-fines'})
        return context

    def get_queryset(self):
        # Get current request
        request = self.request
        # Get query params
        params = request.GET

        # Get the desired page size from the request's GET parameter
        page_size = params.get('page_size', self.paginate_by)
        # Set the paginate_by attribute to the desired page size
        self.paginate_by = page_size

        queryset = super().get_queryset()      
                  
        # Filter results
        if 'q' in params:
            queryset = queryset.filter(
                Q(user__first_name__icontains = params['q']) |
                Q(user__middle_name__icontains = params['q']) |
                Q(user__last_name__icontains = params['q']) |
                Q(activity__name__icontains = params['q']) |
                Q(activity__group__name__icontains = params['q'])
            )
        
        return queryset
    
class FinesByUser(LoginRequiredMixin, ListView):
    template_name = 'client/admin/fine/list_by_user.html'
    queryset = Fine.objects.all()
    paginate_by = 10
    ordering = ('-modified_at', )
    
    def fines_aggregate(self):
        # user_id from path parameters
        user_id = self.kwargs['user_id']
        
        total_fines = self.queryset.filter(user = user_id).\
            exclude(status = 'removed').\
            aggregate(amount=Sum('amount'))['amount']
            
        paid_fines = self.queryset.filter(user = user_id, status='paid').\
            aggregate(amount=Sum('amount'))['amount']
                        
        unpaid_fines = self.queryset.filter(user = user_id, status='unpaid').\
            aggregate(amount=Sum('amount'))['amount']
            
        return {
            "total_fines": total_fines,
            "paid_fines": paid_fines,
            "unpaid_fines": unpaid_fines
        }
        
    def user_obj(self):
        # user_id from path parameters
        user_id = self.kwargs['user_id']
        user = User.objects.filter(id = user_id).first()
        return user
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'current_page': 'manage-fines'})
        context.update({'fines_aggregate': self.fines_aggregate()})
        context.update({'fines_user': self.user_obj()})
        
        return context

    def get_queryset(self):
        # user_id from path parameters
        user_id = self.kwargs['user_id']
        
        # Get current request
        request = self.request
        queryset = super().get_queryset()
        queryset = queryset.filter(user = user_id)
        
        # Get query params
        params = request.GET

        # Get the desired page size from the request's GET parameter
        page_size = params.get('page_size', self.paginate_by)
        # Set the paginate_by attribute to the desired page size
        self.paginate_by = page_size
        
        # Filter results
        if 'q' in params:
            queryset = queryset.filter(
                Q(activity__name__icontains = params['q']) |
                Q(activity__group__name__icontains = params['q'])
            )
        return queryset

    


    
