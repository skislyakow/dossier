"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from main.views import home, api_skills, api_projects, api_timeline, api_contact, api_github

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/skills/', api_skills, name='api_skills'),
    path('api/projects/', api_projects, name='api_projects'),
    path('api/timeline/', api_timeline, name='api_timeline'),
    path('api/contact/', api_contact, name='api_contact'),
    path('api/github/', api_github, name='api_github'),
    path('', home, name='home'),
]
