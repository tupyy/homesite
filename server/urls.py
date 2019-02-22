from django.conf.urls import url
from django.contrib import admin

from contract.views import view_contracts, view_contract_pdf
from rest_framework.routers import DefaultRouter
from django.urls import *

from authentication.views import login_view, logout_view
from money.views.api import CategoryViewSet, PaymentViewSet, SubcategoryViewSet, TotalViewSet, RevenuesViewSet
from money.views.index.controller import IndexView
from money.views.payments.controllers import PaymentsIndexView, DeletePaymentView, PaymentView

"""
    Restful urls
"""
router = DefaultRouter()
router.register(r'api/money/category', CategoryViewSet, base_name="money_category")
router.register(r'api/money/subcategory', SubcategoryViewSet, base_name="money_subcategory")
router.register(r'api/money/payment', PaymentViewSet, base_name='money_payment')
router.register(r'api/money/total', TotalViewSet, base_name="payment_total")
router.register(r'api/money/revenues', RevenuesViewSet, base_name="revenues_total")

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
    url(r'^contract/contracts', view_contracts, name="view_contracts"),
    path('contract/view_pdf/<int:id>', view_contract_pdf, name="view_contract_pdf")
]
"""
Main URL patterns
"""
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^money/payment/add$', PaymentView.as_view(), name="money.payment.add"),
    path('money/payment/delete/<int:payment_id>/', DeletePaymentView.as_view(), name="money.payment.delete"),
    path('money/payment/<int:month>/', PaymentsIndexView.as_view(), name="money.payment.view"),
    path('money/payment/update/<int:payment_id>/', PaymentView.as_view(), name="money.payment.update"),
    # path('money/payment/category/total/', category_total, name="category_total"),
    url(r'^$', IndexView.as_view(), name="index")
]

urlpatterns += router.urls
urlpatterns += urlpatterns_account
urlpatterns += urlpatterns_contracts
