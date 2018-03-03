from django.conf.urls import url,include
from django.contrib import admin
from money.views import *
from rest_framework.routers import DefaultRouter
from django.urls import *
from money.views import *
from money.apiViews import CategoryViewSet, PaymentViewSet, SubcategoryViewSet, PaymentOptionViewSet, \
    TotalViewSet
from authentication.views import login_view, logout_view

"""
    Restful urls
"""
router = DefaultRouter()
router.register(r'api/money/category',CategoryViewSet,base_name="money_category")
router.register(r'api/money/subcategory',SubcategoryViewSet,base_name="money_subcategory")
router.register(r'api/money/payment',PaymentViewSet,base_name='money_payment')
router.register(r'api/money/payment_option',PaymentOptionViewSet,base_name='money_payment_option')
router.register(r'api/money/totals',TotalViewSet,base_name="total_view")

"""
    Url patterns for account
"""
urlpatterns_account = [
    url(r'^accounts/login/', login_view, name='login_view'),
    url(r'^accounts/logout/', logout_view, name='logout_view'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]

"""
Main URL patterns
"""
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^money/payment/$',payment,name="payment"),
    url(r'^money/viewpayment/$',month_payments,name="view_month_payments"),
    url(r'^$',index,name="index")
]

urlpatterns += router.urls
urlpatterns += urlpatterns_account



