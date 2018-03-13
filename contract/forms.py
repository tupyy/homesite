import datetime
from django import forms

import settings
from contract.models import Contract


class ContractForm(forms.ModelForm):
    start_date = forms.DateField(initial=datetime.date.today().strftime('%d/%m/%Y'),
                           input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = Contract
        fields = '__all__'