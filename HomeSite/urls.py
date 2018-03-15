from django.conf.urls import url,include
from django.contrib import admin

from contract.views import view_contracts
from money.views import *
from rest_framework.routers import DefaultRouter
from django.urls import *
from money.views import *
from money.apiViews import CategoryViewSet, PaymentViewSet, SubcategoryViewSet
from authentication.views import login_view, logout_view

"""
    Restful urls
"""
router = DefaultRouter()
router.register(r'api/money/category',CategoryViewSet,base_name="money_category")
router.register(r'api/money/subcategory',SubcategoryViewSet,base_name="money_subcategory")
router.register(r'api/money/payment',PaymentViewSet,base_name='money_payment')

"""
    Url patterns for account
"""
urlpatterns_account = [
    url(r'^accounts/login/', login_view, name='login_view'),
    url(r'^accounts/logout/', logout_view, name='logout_view'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]

"""
    Url for contracts
"""
urlpatterns_contracts = [
    url(r'^contract/contracts', view_contracts, name="view_contracts")
]
"""
Main URL patterns
"""
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^money/payment/$',payment,name="payment"),
    path('money/payment/delete/<int:id>/',delete_payment,name="delete_payment"),
    path('money/payment/view/<int:month>/', view_payments, name="view_month_payments"),
    path('money/payment/update/<int:id>/', update_payments2, name="update_payment"),
    url(r'^$',index,name="index")
]


urlpatterns += router.urls
urlpatterns += urlpatterns_account
urlpatterns += urlpatterns_contracts



