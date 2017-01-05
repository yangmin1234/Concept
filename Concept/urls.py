"""Concept URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include, patterns
from django.contrib import admin
from django.http import HttpResponse
from blog.views import blog_sitemap, custom_404, custom_500
from django.contrib.sitemaps.views import sitemap
from django.conf import settings


sitemaps = {
    'blogs': blog_sitemap
}

urlpatterns = [
#URLs
    url(r'^admin/', admin.site.urls),
    url(r'^', include('blog.urls')),
    url(r'^polls/', include('polls.urls', namespace="polls")),
# Django Registration 2.0.3
    url(r'^accounts/', include('registration.backends.hmac.urls')),
# robots.txt
    url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow:", content_type="text/plain")),
# Sitemap
    #url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
    name='django.contrib.sitemaps.views.sitemap')

]

if settings.DEBUG is False:   #if DEBUG is True it will be served automatically
    urlpatterns += patterns('',
            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )

# #handelers
# handler404 = 'views.custom_404'

# handler500 = 'views.custom_500'