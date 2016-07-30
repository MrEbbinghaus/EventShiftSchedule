from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^mylogin$', views.login_user),
    url(r'^$', views.login, name='login'),
]