from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hello.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/', 'tasktracker.views.home'),
    url(r'^home_submit/', 'tasktracker.views.home_submit'),
    url(r'^task/([0-9]+)/', 'tasktracker.views.task'),
    url(r'^user/(.+)/', 'tasktracker.views.user'),
    url(r'^userlist', 'tasktracker.views.userlist'),
    url(r'^login', 'django.contrib.auth.views.login'),
)
