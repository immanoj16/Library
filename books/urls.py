from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views as core_views


urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'books/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^addbook/', core_views.addbook, name='addbook'),
]