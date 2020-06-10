from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^gold-card-qualification/$', views.goldcardqualification, name='gold-card-qualification'),
    url(r'^gold-card-qualification/(?P<tree_id>[0-9]+)/$', views.goldcardqualificationtree, name='gold-card-qualification-tree'),
    url(r'^gold-card-qualification/results/$', views.goldcardqualificationresults, name='gold-card-qualification-results'),
    url(r'^visa/(?P<visa>[\w|\W]+)/$', views.visa, name='visa'),
    url(r'^(?P<visa_category>[\w|\W]+)/$', views.category, name='category'),
]
