
from django.contrib import admin
from django.urls import path
from . import views
from problemset.views import problemset,tags

urlpatterns = [
    path('',views.home,name='home'),
    path('admin/', admin.site.urls),
    path('problemset/',problemset,name='problemset'),
    path('contests/',views.contests),
    path('problemset/tags/',tags ,name='tags'),
    path('login/',views.login_view,name='login_view'),
    path('registration/',views.registration,name='registration'),
    path('register/',views.register,name='register'),
]