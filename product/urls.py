from django.conf.urls import include, url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', views.ProductList.as_view(), name='products'),
    url(r'^create_product/$', views.CreateProduct.as_view(), name='create_product'),
    url(r'^product_details/(?P<slug>[-a-zA-Z0-9]+)/$', views.ProductDetail.as_view(), name='product_detail'),
    url(r'^product_details/(?P<slug>[-a-zA-Z0-9]+)/like/$', login_required(views.LikeProduct.as_view()), name='like_product'),
]
