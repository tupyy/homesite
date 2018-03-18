from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from contract.models import Contract


@login_required
def view_contracts(request):
    contracts = Contract.objects.order_by("status")
    return render(request, 'contract/view_contract.html', {'contracts': contracts})


@login_required
def view_contract_pdf(request, id=None):
    contract = get_object_or_404(Contract, pk=id)
    return redirect("/media/" + contract.pdf_contract.name)

