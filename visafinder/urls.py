from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^visa/(?P<visa>\w+)/$', views.visa, name='visa'),
    url(r'^(?P<visa_category>\w+)/$', views.category, name='category'),
]
