from django import forms
from django.contrib.auth.models import User

from authentication.models import Account
from money.models import Category,Subcategory,PaymentOption,PaymentModel,PermanentPaymentModel
import datetime

class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentModel
        fields = '__all__'

    next_url = forms.CharField(max_length=200)
    user = forms.ModelChoiceField(label="Name",queryset=User.objects.all(),empty_label=None)
    category = forms.ModelChoiceField(queryset = Category.objects.all(),empty_label=None)
    subcategory = forms.ModelChoiceField(queryset=Subcategory.objects.all(),empty_label=None)

    sum = forms.DecimalField(max_digits=5,decimal_places=2,label="Suma",min_value=0)
    option_pay = forms.ModelChoiceField(queryset=PaymentOption.objects.all(),empty_label=None)
    nb_option = forms.IntegerField(label='Numar optiuni de plata',min_value=0,initial=0)
    date = forms.DateField(initial=datetime.date.today().strftime('%d/%m/%Y'),input_formats=['%d/%m/%Y'])

    comments = forms.CharField(
        max_length=150,
        widget=forms.Textarea(),
        help_text="Comentariu",
        required=False
    )


class PermanentPaymentForm(forms.Form):
    user = forms.ModelChoiceField(label="User",queryset=User.objects.all(),empty_label=None)
    category = forms.ModelChoiceField(queryset = Category.objects.all(),empty_label=None)

    subcategories = Subcategory.objects.filter(category__name__exact='Alimente')
    subcategory = forms.CharField(required=False,widget=forms.Select(choices=( x.name for x in subcategories )))

    suma = forms.DecimalField(max_digits=5,decimal_places=2,label="Suma",min_value=0)
    comments = forms.CharField(
        max_length=200,
        widget=forms.Textarea(),
        help_text="Comentariu",
        required=False
    )

    def save(self):
        data = self.cleaned_data
        payment = PermanentPaymentModel(user=data['user'],
                               category=data['category'],
                               subcategory=Subcategory.objects.get(pk=int(data['subcategory'])),
                               sum=data['suma'],
                               comments=data['comments'])
        payment.save()

