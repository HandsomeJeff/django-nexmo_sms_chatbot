from django.conf.urls import url

from . import views

app_name = "botsite"

urlpatterns = [
    url(r'^$', views.request_msg, name='request_msg'),
]
