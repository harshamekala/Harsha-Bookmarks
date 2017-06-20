from django.conf.urls import url
from bookmarks.views import *

urlpatterns = [
    url(r'^registration/$', Registration, name = "Register"),
    url(r'^login/$', login_view, name = "login"),
    url(r'^logout/$', logout_view, name = "logout"),
    url(r'^addbookmark/$', addbookmark, name = "addbookmark"),
    url(r'^editbookmark/(?P<pk>\d+)/$', BookmarkUpdateView.as_view(), name = "editbookmark"),
    url(r'^home/$', Homepage, name= "homepage"),
    url(r'^user/(\w+)/$', userpage, name = "user"),
    url(r'^tag/(\w+)/$', tagpage, name = "tag"),
    url(r'^vote/(?P<pk>\d+)/$', votepage, name = "vote"),
    url(r'^search/', search, name = "search"),

]
