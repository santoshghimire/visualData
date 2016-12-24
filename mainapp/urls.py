"""Urls for Academics."""
from django.conf.urls import url

from .views import (
    WordCloudAPI, WordTreeAPI, UniqueUsersAPI,
    VisualizationView
)

urlpatterns = [
    url(
        regex=r'^api/users/',
        view=UniqueUsersAPI.as_view(),
        name='uniqueusers_api'
    ),
    url(
        regex=r'^api/wordcloud/(?P<username>[-\w]+)',
        view=WordCloudAPI.as_view(),
        name='wordcloud_api'
    ),
    url(
        regex=r'^api/wordtree/(?P<username>[-\w]+)',
        view=WordTreeAPI.as_view(),
        name='wordtree_api'
    ),
    url(
        r'^visualization/(?P<username>[-\w]+)/$',
        view=VisualizationView.as_view(),
        name='visualization'),
]
