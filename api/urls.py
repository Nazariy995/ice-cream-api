from django.conf.urls import patterns, include, url
from api.routes import views as routesViews
from api.upload import views as uploadViews
from api.warehouse_inventory import views as warehouseInventoryViews
from api.default_inventory import views as defaultInventoryViews
from rest_framework.authtoken import views

urlpatterns = patterns('',

                       url(r'^routes/$', routesViews.Routes.as_view()),
                       url(r'^upload/$', uploadViews.Upload.as_view()),
                       url(r'^login/$', views.obtain_auth_token),
                       url(r'^warehouseinventory/$', warehouseInventoryViews.WarehouseInventoryView.as_view()),
                       url(r'^defaultinventory/$', defaultInventoryViews.DefaultInventoryView.as_view())

)
