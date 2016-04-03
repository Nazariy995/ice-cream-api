from django.conf.urls import patterns, include, url
from api.routes import views as routesViews

urlpatterns = patterns('',

                       url(r'^routes/$', routesViews.Routes.as_view())


)
