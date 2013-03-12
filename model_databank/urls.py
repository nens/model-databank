# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.contrib import admin
from django.views.generic import TemplateView

#from lizard_ui.urls import debugmode_urlpatterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from model_databank import views

admin.autodiscover()

urlpatterns = patterns(
    '',
#    url(r'^$', TemplateView.as_view(
#        template_name='model_databank/index.html'),
#        name='index'),
    # formerly r'^models/$'
    url(r'^$', views.ModelReferenceList.as_view(),
        name='model_reference_list'),
    url(r'^upload_new/$', views.NewModelUploadFormView.as_view(),
        name='upload_form'),
    url(r'^models/(?P<pk>\d+)/download/$',
        views.ModelDownloadView.as_view(),
        name='model_reference_download'),
    url(r'^models/(?P<pk>\d+)/commits/(?P<revision>\w+)/$',
        views.CommitView.as_view(),
        name='commit_view'),
    url(r'^models/(?P<pk>\d+)/commits/$', views.ModelReferenceDetail.as_view(),
        name='model_reference_detail'),

#    url(r'^ui/', include('lizard_ui.urls')),
    # url(r'^map/', include('lizard_map.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^something/',
    #     views.some_method,
    #     name="name_it"),
    # url(r'^something_else/$',
    #     views.SomeClassBasedView.as_view(),
    #     name='name_it_too'),
    )
#urlpatterns += debugmode_urlpatterns()
urlpatterns += staticfiles_urlpatterns()
