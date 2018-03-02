import django_tables2 as tables
from django.utils.html import escape
from django.utils.safestring import mark_safe

from money.models import PaymentModel,PermanentPaymentModel


class DeleteButtonColumn(tables.Column):

    def set_url(self,url):
        self.my_url = url

    empty_values = list()
    def render(self, value, record):
        return mark_safe('<a href="/'+self.my_url+'/%s/" class="btn btn-info" role="button">Delete</a>' % escape(record.id))


class MonthTable(tables.Table):
    submit = DeleteButtonColumn(verbose_name= '')
    submit.set_url('delete_payment')

    class Meta:
        model = PaymentModel
        row_attrs = {
            'data-id': lambda record: record.pk
        }
        exclude = {
            'id'
        }
        attrs = {
            'class': 'table table-condensed',

        }

    def getMonth(self,date):
        return date.month(date)


class ViewPermanentPaymentTable(tables.Table):
    """
    It shows the permanent payments
    """
    submit = DeleteButtonColumn(verbose_name= '' )
    submit.set_url('delete_permanent_payment')

    class Meta:
        model = PermanentPaymentModel
        row_attrs = {
            'data-id': lambda record: record.pk
        }
        exclude = {
            'id'
        }
        attrs = {
            'class': 'table table-condensed',

        }

    def getMonth(self,date):
        return date.month(date)

class TotalTable(tables.Table):
    categorie = tables.Column()
    suma = tables.Column()

    class Meta:
        attrs = {'class' : 'table table-condensed'}