from django.contrib import admin
from django.conf.urls import url,include

# from django.urls import path
from shop.views.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^home',view=home ,name='home'),
    url(r'^placeOrder/(?P<id>[\w.@+-]+)/$', view=placeOrder, name='placeOrder'),
    url(r'^login/$', loginPage,name='login'),
    url(r'^logout/$' ,logoutPage,name='logout'),
    url(r'^register/', registerPage,name='register'),
    url(r'^addProduct/', addProduct,name='addProduct'),
    url(r'^download_media/(?P<filename>[\w.@+-]+)$',download_media,name='download_media'),
    url(r'^addToCart/(?P<pid>[\w.@+-]+)/(?P<cid>[\w.@+-]+)$',addToCart,name='addToCart'),
    url(r'^getCartItem/(?P<cid>[\w.@+-]+)$',getCartItem,name='getCartItem'),
    url(r'^checkout/(?P<cid>[\w.@+-]+)$',checkout,name='checkout'),
    ]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)