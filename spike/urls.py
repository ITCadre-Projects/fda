from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^fda$', views.fda, name='fda'),
	url(r'^search-form/$', views.search_form, name='search_form'),
	url(r'^search/$', views.search, name='search'),
	url(r'^get-drug-names/$', views.get_drug_names, name='get_drug_names'),
]