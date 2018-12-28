from django.urls import path
from .views.Dataviews import FetchDataView

app_name = 'udata'

urlpatterns = [
    path('search/', FetchDataView.as_view(), name='fetch-data'),
]
