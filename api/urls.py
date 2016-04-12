from django.conf.urls import patterns, include, url
from api.routes import views as routesViews
from rest_framework.authtoken import views

urlpatterns = patterns('',

                       url(r'^routes/$', routesViews.Routes.as_view()),
                       url(r'^login/$', views.obtain_auth_token),
)
