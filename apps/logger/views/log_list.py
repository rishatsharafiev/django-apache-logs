from django.views.generic import ListView
from utils.views import SearchListView

from ..models import Log
from ..forms import SearchForm
from django.contrib.postgres.search import SearchVector

from django.db.models import Q, Count, Sum

class LogListView(SearchListView):
    """Log List View"""

    form_class = SearchForm
    paginate_by = 8

    def get_initial(self):
        return { 'search': self.search }

    def dispatch(self, request, *args, **kwargs):
        self.search = self.request.GET.get('search', '')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_obj = context['page_obj']

        index = page_obj.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 3 if index >= 3 else 0
        end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = paginator.page_range[start_index:end_index]

        context['page_range'] = page_range

        queryset = self.get_queryset()
        
        # aggreagation
        context['unique_ip_address_count'] = queryset.order_by('ip_address').distinct('ip_address').count()
        context['ip_address_counts'] = queryset.values('ip_address').annotate(total=Count('ip_address')).order_by('-total')[:10]
        context['method_counts'] = queryset.values('method').annotate(total=Count('method')).order_by('-total')
        context['total_size'] = queryset.aggregate(total_size=Sum('size')).get('total_size')

        return context

    def get_queryset(self):
        return Log.objects.filter(
            Q(method__icontains=self.search) |
            Q(code__icontains=self.search) |
            Q(ip_address__icontains=self.search) |
            Q(uri__icontains=self.search)
        )
        return Log.objects.annotate(search=SearchVector('ip_address', 'method', 'uri', 'code',)).filter(search=self.search)
