from django.db.models import Q
from django.views.generic import ListView

from api.models import ActivityGroup, Activity

from . custom_mixins import AdminRequiredMixin, LoginRequiredMixin

__all__ = ['ActivityGroupList', 'ActivityList', 'ActivityOnGoing'] 

class ActivityGroupList(AdminRequiredMixin, ListView):
    template_name = 'client/admin/activity/list_group.html'
    queryset = ActivityGroup.objects.all()
    paginate_by = 10
    ordering = ('-created_at', )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'current_page': 'manage-activities'})
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
                Q(name__icontains = params['q'])|
                Q(description__icontains = params['q'])
            )
        return queryset
    
class ActivityList(AdminRequiredMixin, ListView):
    template_name = 'client/admin/activity/list.html'
    queryset = Activity.objects.all()
    paginate_by = 10
    ordering = ('-created_at', )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'current_page': 'manage-activities'})
        context.update({'group': ActivityGroup.objects.filter(id = self.kwargs['group']).first()})
        return context

    def get_queryset(self):
        # filter based on group        
        queryset = super().get_queryset().filter(group = self.kwargs['group'])
        # Get current request
        request = self.request
        # Get query params
        params = request.GET

        # Get the desired page size from the request's GET parameter
        page_size = params.get('page_size', self.paginate_by)
        # Set the paginate_by attribute to the desired page size
        self.paginate_by = page_size

        # Filter results
        if 'q' in params:
            queryset = queryset.filter(
                Q(name__icontains = params['q'])|
                Q(start_time__icontains = params['q'])|
                Q(end_time__icontains = params['q'])
            )
        return queryset
    
class ActivityOnGoing(LoginRequiredMixin, ListView):
    template_name = 'client/on-going-activities.html'
    queryset = Activity.objects.all()
    paginate_by = 10
    ordering = ('-created_at', )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'current_page': 'on-going-activities'})
        return context

    def get_queryset(self):
        # filter based on group        
        queryset = super().get_queryset().filter(status='open')
        # Get current request
        request = self.request
        # Get query params
        params = request.GET

        # Get the desired page size from the request's GET parameter
        page_size = params.get('page_size', self.paginate_by)
        # Set the paginate_by attribute to the desired page size
        self.paginate_by = page_size

        # Filter results
        if 'q' in params:
            queryset = queryset.filter(
                Q(name__icontains = params['q'])|
                Q(group__name__icontains = params['q'])|
                Q(start_time__icontains = params['q'])|
                Q(end_time__icontains = params['q'])
            )
        return queryset


    
