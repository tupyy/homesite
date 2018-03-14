from django.contrib import admin

# Register your models here.
from contract.models import ContractType, ContractStatus, Contract

admin.site.register(ContractType)
admin.site.register(ContractStatus)

@admin.register(Contract)
class ContractModelAdim(admin.ModelAdmin):
    list_display = ('name','contract_type','company_name','contract_id','start_date','status')
    exclude = ('id',)
    list_filter = ('name','contract_type','company_name')
    search_fields = ['name', 'contract_type','company_name']