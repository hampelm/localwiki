from django.conf.urls.defaults import *

from utils.constants import DATETIME_REGEXP

from views import (TagUpdateView, TagCompareView, 
    TagDeleteView, TagListView)

urlpatterns = patterns('',
    
    url(r'^(?P<slug>.+)/_delete$',
        TagDeleteView.as_view(), name='delete'),
    url(r'^(?P<slug>.+)/_history/(?P<date1>%s)\.\.\.(?P<date2>%s)?$'
        % (DATETIME_REGEXP, DATETIME_REGEXP),
        TagCompareView.as_view(), name='compare-dates'),
    url(r'^(?P<slug>.+)/', TagUpdateView.as_view(), name='edit'),
    url(r'^(?P<term_slug>.+)', TagListView.as_view(), name='tag'),

)
