from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.pss_landing, name='pss_landing'),
    url(r'^pss/$', views.shift_schedule, name='shift_schedule'),
    url(r'^event/post/enter/$', views.enter, name='enter'),
    url(r'^event/(?P<event_id>[0-9]+)', views.shift_schedule_event, name='shift_schedule_event'),
]