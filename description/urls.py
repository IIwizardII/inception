from django.urls import path
from . import views


urlpatterns = [
    path('', views.show_description, name='get-description'),
    path('description', views.show_description, name='get-description'),

]
