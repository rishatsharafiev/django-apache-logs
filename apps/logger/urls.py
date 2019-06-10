
from django.urls import path

from .views.log_list import LogListView


app_name = 'logger'

urlpatterns = (
    path('', LogListView.as_view(), name='log-list'),
)
