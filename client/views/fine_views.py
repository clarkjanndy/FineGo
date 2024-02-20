from django.db.models import Q
from django.views.generic import ListView

from api.models import Fine

from .custom_mixins import AdminRequiredMixin, LoginRequiredMixin

__all__ = ['UserFines', 'FineList'] 

class UserFines(LoginRequiredMixin, ListView):
    template_name = 'client/my-fines.html'
    queryset = Fine.objects.all()
    paginate_by = 10
    ordering = ('-modified_at', )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'current_page': 'my-fines'})
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
                Q(activity__group__name__icontains = params['q']) |
                Q(amount__icontains = params['q'])
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
                Q(activity__group__name__icontains = params['q']) |
                Q(amount__icontains = params['q'])
            )
        return queryset

    


    
