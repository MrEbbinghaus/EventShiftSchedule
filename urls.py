from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ess_landing, name='home'),
    url(r'^event/post/enter/$', views.enter, name='enter'),
    url(r'^event/post/comment/$', views.add_comment, name='comment'),
    url(r'^event/post/enter/otp/$', views.enter_otp, name='enter_otp'),
    url(r'^event/(?P<event_id>[0-9]+)', views.shift_schedule_event, name='shift_schedule_event'),
]
