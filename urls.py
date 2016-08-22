from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.pss_landing, name='pss_landing'),
    url(r'^pss/$', views.shift_schedule, name='shift_schedule'),
    url(r'^pss/post/enter/$', views.enter, name='enter'),
]