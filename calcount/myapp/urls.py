
from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),
    path('userprofile_update/', userprofile_update, name='userprofile_update'),
    path('register/', register, name='register'),
    path('', loginpage, name='loginpage'),
    path('logout/', logoutpage, name='logoutpage'),
    path('update_consumed_items/<int:id>', update_consumed_items, name='update_consumed_items'),
    path('delete_item/<int:id>', delete_item, name='delete_item'),
    
    path('activate/<uid64>/<token>', activate,name='activate'),
    
    
    path('forgetpassword/', forgetpassword, name="forgetpassword"),
    path('changepassword/', changepassword, name="changepassword"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
