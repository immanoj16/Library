from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views as core_views


urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'books/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^addbook/', core_views.addbook, name='addbook'),
    url(r'^search/$', core_views.search, name='search'),
    url(r'^profile/', core_views.profile, name='profile'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^(?P<book_id>[0-9]+)/', core_views.issue, name='issue'),
    url(r'^issue_list', core_views.issue_list, name='issue_list'),
]