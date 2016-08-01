from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.foo, name='foo'),
    url(r'^pss/$', views.shift_schedule, name='shift_schedule')
]