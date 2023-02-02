"""ratingapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rating.views import login, signup, editapps, edituserprofile, homeview, usertasks, admin_user_tasks, userprofile, adminlogin,adminsignup
from knox.views import LogoutView, LogoutAllView
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from . import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="user-appcredits",
      default_version='v1',
      description="Test",
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)



urlpatterns = [
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('signup',signup.as_view()), # user signup
    path('adminsignup',adminsignup.as_view()), # admin sign up where only authenticated admin user can create another admin user
    path('login',login.as_view()), # user login
    path('adminlogin',adminlogin.as_view()), # admin login
    path('logout',LogoutView.as_view()), # logout for both admin and user
    path('logoutall',LogoutAllView.as_view()), # logout from all devices for both admin and user
    path('home',homeview.as_view()), # returns all apps
    path('userprofile',userprofile.as_view()), # returns the profile detail and apps and points of the logged in user
    path('usertasks',usertasks.as_view()), # returns the tasks of the logged in user 
    path('editapps',editapps.as_view()), # admin adds and gets all aapps
    path('editapps/<int:id>', editapps.as_view()), # admin can edit and delete app
    path('edituserprofile',edituserprofile.as_view()), # admin can get, add , edit and delete userprofile
    # path('edituserprofile/<int:id>', edituserprofile.as_view()),   
    # path('adminedittasks/<int:id>',admin_user_tasks.as_view()),    
    path('adminedittasks',admin_user_tasks.as_view()), # admin can get, edit and delete tasks
    
]

urlpatterns += static('scrn', document_root=settings.BASE_DIR/'scrn')
print(settings.BASE_DIR)

