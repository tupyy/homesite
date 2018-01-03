from django.conf.urls import url,include
from django.contrib import admin
from money.views import *
from rest_framework.routers import DefaultRouter
from django.urls import *
from money.views import *
from money.apiViews import CategoryViewSet,PaymentViewSet,SubcategoryViewSet
from django.contrib.staticfiles.views import serve
from django.conf.urls.static import static
import settings


router = DefaultRouter()
router.register(r'api/money/category',CategoryViewSet,base_name="money_category")
router.register(r'api/money/subcategory',SubcategoryViewSet,base_name="money_subcategory")
router.register(r'api/money/payment',PaymentViewSet,base_name='money_payment')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^api/subcategories/(?P<category>.+)/$', SubcategoryViewSet.as_view({'get':'category'})),
    url(r'^payment/',payment,name="payment"),
    url(r'^permanent_payment/',permanent_payment,name='permanent_payment'),
    url(r'^delete_payment/(?P<pk>[0-9]+)/$',delete_payment,name="delete_payment"),
    url(r'^month/',month_payments,name='month'),
    url(r'^view_permanent_payments/',view_permanent_payments,name="view_permanent_payments"),
    url(r'^delete_permanent_payment/(?P<pk>[0-9]+)/$', delete_permanent_payment, name="delete_permanent_payment"),

    url(r'^$',index,name="index")
]

urlpatterns += router.urls

#urlpatterns += router.urls

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    url(r'^accounts/', include('django.contrib.auth.urls')),
]



