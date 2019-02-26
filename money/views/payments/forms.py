import datetime

from django import forms
from django.contrib.auth.models import User

import server.settings
from money.models import Category, Subcategory, Payment


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ('__all__')

    next_url = forms.CharField(max_length=200)
    user = forms.ModelChoiceField(label="Name", queryset=User.objects.all(), empty_label=None)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)
    subcategory = forms.ModelChoiceField(queryset=Subcategory.objects.all(), empty_label=None)
    date = forms.DateField(initial=datetime.date.today().strftime('%d/%m/%Y'),
                           input_formats=server.settings.DATE_INPUT_FORMATS)

    comments = forms.CharField(
        max_length=120,
        widget=forms.Textarea(),
        help_text="Comentariu",
        required=False
    )