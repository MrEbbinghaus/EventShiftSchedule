from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.pss_landing, name='pss_landing'),
    url(r'^pss/$', views.shift_schedule, name='shift_schedule'),
    url(r'^pss_enter/$', views.shift_schedule_enter, name='shift_schedule_enter'),
    url(r'^pss_enter/post/enter/$', views.enter, name='enter'),
]