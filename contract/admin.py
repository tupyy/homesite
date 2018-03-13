from django.contrib import admin

# Register your models here.
from contract.models import ContractType, ContractStatus, Contract

admin.site.register(ContractType)
admin.site.register(ContractStatus)
admin.site.register(Contract)