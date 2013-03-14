# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.contrib import admin

#from lizard_ui.urls import debugmode_urlpatterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from model_databank import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.ModelReferenceList.as_view(),
        name='model_reference_list'),
    url(r'^upload_new/$', views.NewModelUploadFormView.as_view(),
        name='upload_form'),
    url(r'^models/(?P<slug>[\w-]+)/download/$',
        views.ModelDownloadView.as_view(),
        name='model_reference_download'),
    url(r'^models/(?P<slug>[\w-]+)/commits/(?P<revision>\w+)/$',
        views.CommitView.as_view(),
        name='commit_view'),
    url(r'^models/(?P<slug>[\w-]+)/commits/$',
        views.ModelReferenceDetail.as_view(),
        name='model_reference_detail'),

    url(r'^models/(?P<slug>[\w-]+)/files/$', views.FilesView.as_view(),
        name='model_reference_files'),

    url(r'^admin/', include(admin.site.urls)),
)
#urlpatterns += debugmode_urlpatterns()
urlpatterns += staticfiles_urlpatterns()
