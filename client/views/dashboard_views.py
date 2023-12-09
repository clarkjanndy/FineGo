from django.views.generic import TemplateView
from .custom_mixins import AdminRequiredMixin

__all__ = ['DashboardView']

class DashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'client/admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'current_page': 'admin-dashboard'})

        return context