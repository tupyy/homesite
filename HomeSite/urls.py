from django.conf.urls import url,include
from django.contrib import admin
from money.views import *
from rest_framework.routers import DefaultRouter
from django.urls import *
from money.views import *
from money.apiViews import CategoryViewSet,PaymentViewSet,SubcategoryViewSet,PaymentOptionViewSet
from authentication.views import AccountViewSet,LoginView,LogoutView

router = DefaultRouter()
router.register(r'api/money/category',CategoryViewSet,base_name="money_category")
router.register(r'api/money/subcategory',SubcategoryViewSet,base_name="money_subcategory")
router.register(r'api/money/payment',PaymentViewSet,base_name='money_payment')
router.register(r'api/money/payment_option',PaymentOptionViewSet,base_name='money_payment_option')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^api/subcategories/(?P<category>.+)/$', SubcategoryViewSet.as_view({'get':'category'})),
    url(r'^auth/login/$', LoginView.as_view(), name='login'),
    url(r'^auth/logout/$', LogoutView.as_view(), name='logout'),
    url(r'^$',index,name="index")

]

urlpatterns += router.urls



