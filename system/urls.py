from django.urls import path
from .views import *

app_name = 'system'

urlpatterns = [
    path('save', save_data, name='saving_data'),
    path('parent', parent_view, name='add new parent'),
    path('child', child_view, name='add new child'),
]