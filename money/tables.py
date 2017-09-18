import django_tables2 as tables
from models import PaymentModel

class MonthTable(tables.Table):
    class Meta:
        model = PaymentModel
        row_attrs = {
            'data-id': lambda record: record.pk
        }
        exclude = {
            'id'
        }
