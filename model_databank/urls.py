# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework.urlpatterns import format_suffix_patterns

from model_databank import views

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.ModelReferenceList.as_view(),
        name='model_reference_list'),
    url(r'^upload_new/$', views.ModelUploadFormView.as_view(),
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
]

api_urlpatterns = [
    url(r'^api/models/$', views.ApiModelReferenceList.as_view(),
        name='api_model_reference_list'),
]
urlpatterns += format_suffix_patterns(api_urlpatterns)
urlpatterns += staticfiles_urlpatterns()
