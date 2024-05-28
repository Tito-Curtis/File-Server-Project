"""
URL configuration for fileserver project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from file import urls
from django.contrib.auth import views as auth_views
from file.views import CustomPasswordResetConfirmView,CustomPasswordResetView,error_404_view,error_500_view
from file.forms import CustomSetPasswordsForm   

urlpatterns = [                                             
    path('admin/', admin.site.urls),
    path('', include(urls)),
    path('reset_password/',CustomPasswordResetView.as_view(),
        name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='reset_password_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',CustomPasswordResetConfirmView.as_view(),
          name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='reset_pass_complete.html'), 
         name='password_reset_complete'),
]

handler404 = error_404_view
handler500 = error_500_view

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()