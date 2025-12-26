from django.urls import path
from .views import index, by_rubric, BbCreateView
from .views import async_ping

urlpatterns = [
    path('', index, name='index'),
    path('rubric/<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('add/', BbCreateView.as_view(), name='add'),
    path('async/', async_ping, name='async_ping'),
]
