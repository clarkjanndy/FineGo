from django.db.models import Q
from django.db.models.base import Model as Model
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.http import Http404

from api.models import ActivityGroup, Activity, Attendance

from . custom_mixins import AdminRequiredMixin, LoginRequiredMixin

__all__ = ['ActivityGroupList', 'ActivityList', 'ActivityDetails', 'ActivityOnGoing'] 

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
    
class ActivityDetails(AdminRequiredMixin, DetailView):
    template_name = 'client/admin/activity/detail.html'
    queryset = Activity.objects.select_related('group')
    context_object_name = 'activity'
    
    def get_queryset(self):
        # filter based on group        
        queryset = super().get_queryset().filter(group = self.kwargs['group'])
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        params = request.GET
        
        # pagination context data
        page_size = params.get('page_size', 10)
        page = params.get('page', 1)
        attedances = Attendance.objects.filter(activity=self.kwargs['pk']).order_by('created_at')
         # Filter results
        if 'q' in params:
            attedances = attedances.filter(
                Q(user__first_name__icontains = params['q'])|
                Q(user__middle_name__icontains = params['q'])|
                Q(user__last_name__icontains = params['q'])|
                Q(user__suffix__icontains = params['q'])
            )  
        try:
            paginator = Paginator(attedances, page_size) 
            page_obj = paginator.page(page)
            
        except:
            raise Http404()
        
        context.update({'page_obj': page_obj})
        context.update({'paginator': paginator})    
        context.update({'current_page': 'manage-activities'})
        return context
    
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


    
