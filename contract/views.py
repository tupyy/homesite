from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from contract.models import Contract


@login_required
def view_contracts(request):
    contracts = Contract.objects.order_by("status")
    return render(request, 'contract/view_contract.html', {'contracts': contracts})