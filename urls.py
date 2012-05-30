from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'farcon.views.home', name='home'),
    url(r'^login/', 'farcon.views.login', name='login'),
    url(r'^js/adduser', 'farcon.views.register', name='register'),
    url(r'^logout/', 'farcon.views.logout', name='logout'),
    url(r'^manage/(?P<primary_key>\w+)/$', 'session_manager.views.manage_view', name='manage'),
    url(r'^admin/', include(admin.site.urls)),
)
