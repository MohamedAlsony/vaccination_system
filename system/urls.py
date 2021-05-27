from django.urls import path
from .views import *

app_name = 'system'

urlpatterns = [
    path('save', save_data, name='saving_data'),
    path('parent', parent_view, name='add new parent'),
    path('child', child_view, name='add new child'),
    path('mail', child_vaccine_view, name='mail'),
    path('seen/<int:parent>/<int:vaccine>', seen_by_parent_view),
]