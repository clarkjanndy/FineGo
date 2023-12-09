from django.db.models import Q
from django.views.generic import ListView

from api.models import FAQ

from .custom_mixins import AdminRequiredMixin, LoginRequiredMixin

__all__ = ['FAQList', 'FAQ'] 

class FAQList(AdminRequiredMixin, ListView):
    template_name = 'client/admin/faq/list.html'
    queryset = FAQ.objects.all()
    paginate_by = 10
    ordering = ('-modified_at', )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'current_page': 'manage-faqs'})
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
                Q(question__icontains = params['q']) |
                Q(answer__icontains = params['q'])
            )
        return queryset

class FAQ(ListView, LoginRequiredMixin):
    template_name = 'client/faq.html'
    queryset = FAQ.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'current_page': 'faq'})
        return context
    


    
