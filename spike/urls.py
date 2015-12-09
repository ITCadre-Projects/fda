from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^fda$', views.fda, name='fda'),
    url(r'^$', views.search_form, name='search_form'),
    url(r'^search/$', views.search, name='search'),
    url(r'^get-drug-names/$', views.get_drug_names, name='get_drug_names'),
    url(r'^search-mentioned-events-twitter/$', views.search_mentioned_events_twitter,
        name='search_mentioned_events_twitter')
]

urlpatterns = format_suffix_patterns(urlpatterns)
