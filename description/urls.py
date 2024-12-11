from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.show_description, name='get-description'),
    path('description', views.show_description, name='get-description'),
    # path('interfaceconfig', views.interface_config, name='interface-config'),
    re_path(r'^interface-config/(?P<value>.+)/$', views.interface_config, name='interface-config'),
    
    
    
    
    path('check', views.check_env_variable, name='check'),

]
