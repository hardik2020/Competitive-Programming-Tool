
from django.contrib import admin
from django.urls import path,re_path
from . import views
from problemset.views import problemset,tags
from django.conf.urls import url

urlpatterns = [

    path('',views.home,name='home'),
    path('admin/', admin.site.urls),
    path('problemset/',problemset,name='problemset'),
    path('contests/',views.contests),
    path('problemset/tags/',tags ,name='tags'),
    path('login/',views.login_view,name='login_view'),
    path('logout/',views.logout_view,name='logout_view'),
    path('registration/',views.registration,name='registration'),
    path('register/',views.register,name='register'),
    path('load/<int:id>/<int:range1>/<int:range2>',views.load,name='load'),
]