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
    url(r'^tasks/([0-9]+)/', 'tasktracker.views.task'),
    url(r'^users/(.+?)/', 'tasktracker.views.user'),
    url(r'^profile/', 'tasktracker.views.profile'),
    url(r'^userlist/', 'tasktracker.views.userlist'),
    url(r'^login/', 'tasktracker.views.login_view'),
    url(r'^register/', 'tasktracker.views.registration_view'),
    url(r'^login_submit/', 'tasktracker.views.login_view_post'),
    url(r'^user_logout/', 'tasktracker.views.logout_view'),
)
