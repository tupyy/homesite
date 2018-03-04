from django import forms
from django.contrib.auth.models import User

from authentication.models import Account
from money.models import Category,Subcategory,PaymentOption,PaymentModel,PermanentPaymentModel
import datetime

class SubcategoryModelChoice(forms.ModelChoiceField):
    def to_python(self, value):
        return value

class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentModel
        fields = '__all__'

    user = forms.ModelChoiceField(label="Name",queryset=User.objects.all(),empty_label=None)
    category = forms.ModelChoiceField(queryset = Category.objects.all(),empty_label=None)
    subcategory = SubcategoryModelChoice(queryset=Subcategory.objects.all(),empty_label=None)

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

    def clean(self):
        cleaned_data = super(PaymentForm,self).clean()
        category_name = self.cleaned_data.get('category')
        subcategory_id = self.data.get('subcategory')
        try:
            subcategory_key = int(subcategory_id)
            try:
                subcategory = Subcategory.objects.get(category__name__exact=category_name, id__exact=subcategory_key)
                cleaned_data['subcategory'] = subcategory
            except Subcategory.DoesNotExist:
                raise forms.ValidationError("Subcategory don't exists")
        except ValueError:
            subcategory_name = subcategory_id
            try:
                subcategory = Subcategory.objects.get(category__name__exact=category_name, name__exact=subcategory_name)
                cleaned_data['subcategory'] = subcategory
            except Subcategory.DoesNotExist:
                raise forms.ValidationError("Subcategory don't exists")
        return cleaned_data

    def save(self,commit=True):
        data = self.cleaned_data
        payment = PaymentModel(user=data['user'],
                               category=data['category'],
                               subcategory=data['subcategory'],
                               sum=data['sum'],
                               option_pay=data['option_pay'],
                               nb_option=data['nb_option'],
                               date=data['date'],
                               comments=data['comments'])
        if commit:
            payment.save()
        return payment


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

