from django.urls import path,include
from myapp.views import *

urlpatterns = [
    
    path('', include('myapp.urls')),
]
