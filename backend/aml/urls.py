"""aml URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


# Admin strings
admin.site.site_header = "AML Admin"
admin.site.site_title = "AML Admin"
admin.site.index_title = "Welcome to AML Admin"

# Urls patterns
urlpatterns = [
    path('experiment/', include('experiment.urls')),
    path('participant/', include('participant.urls')),
    path('result/', include('result.urls')),
    path('section/', include('section.urls')),
    path('session/', include('session.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#   ^ The static helper function only works in debug mode
# (https://docs.djangoproject.com/en/3.0/howto/static-files/)

# Debug toolbar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
