"""mental_health URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    path('',views.first),
    path('index',views.index),
    path('reg',views.reg),
    path('registration',views.registration),
    path('login',views.login),
    path('logint',views.logint),
    path('logout/',views.logout),
    path('diary',views.diary),
    path('chatbot',views.chatbot),
    path('chat',views.chat,name="chat"),
    path('doctorchat/chatss',views.chatss,name="chatss"),
    path('viewusers',views.viewusers,name="viewusers"),
    path('doctorchat/<int:id>',views.doctorchat,name="doctorchat"),
    path('userchat',views.userchat,name="userchat"),
    path('admin/', admin.site.urls),
]
