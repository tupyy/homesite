from django import forms
from models import Category,Subcategory,PaymentOption,PaymentModel
import datetime
from django.contrib.auth.models import User

class PaymentForm(forms.Form):
    user = forms.ModelChoiceField(label="User",queryset=User.objects.all(),empty_label=None)
    category = forms.ModelChoiceField(queryset = Category.objects.all(),empty_label=None)
    subcategory = forms.ModelChoiceField(
        label="Subcategory",
        queryset=Subcategory.objects.filter(category__name='Alimente'),
        empty_label=None
    )
    suma = forms.DecimalField(max_digits=5,decimal_places=2,label="Suma",min_value=0)
    payment_option = forms.ModelChoiceField(queryset=PaymentOption.objects.all(),empty_label=None)
    nb_payment_option = forms.IntegerField(label='Numar optiuni de plata',min_value=0,initial=0)
    date = forms.DateField(initial=datetime.date.today().strftime('%d/%m/%y'),input_formats=['%d/%m/%y'])

    comments = forms.CharField(
        max_length=200,
        widget=forms.Textarea(),
        help_text="Comentariu",
        required=False
    )

    def save(self):
        data = self.cleaned_data
        payment = PaymentModel(user=data['user'],
                               category=data['category'],
                               subcategory=data['subcategory'],
                               sum=data['suma'],
                               option_pay=data['payment_option'],
                               nb_option=data['nb_payment_option'],
                               date=data['date'],
                               comments=data['comments'])
        payment.save()

