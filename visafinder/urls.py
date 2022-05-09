from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gold-card-qualification/', views.goldcardqualification, name='gold-card-qualification'),
    re_path(r'^gold-card-qualification/(?P<tree_id>[0-9]+)/$', views.goldcardqualificationtree, name='gold-card-qualification-tree'),
    path('gold-card-qualification/results/', views.goldcardqualificationresults, name='gold-card-qualification-results'),
    re_path(r'^visa/(?P<visa>[\w|\W]+)/$', views.visa, name='visa'),
    re_path(r'^(?P<visa_category>[\w|\W]+)/$', views.category, name='category'),
]
