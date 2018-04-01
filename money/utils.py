import datetime
from calendar import monthrange

from money.models import PaymentOccurrence, RecurrentPayment
from operator import itemgetter


def format_number(number):
    return "{:4.1f}".format(number)


def process_occurrences(occurrences_gen):
    """
    For each occurrence return a list of payments id
    :param occurrences_gen:
    :return: list of payment object and date of occurrence
    """

    ids = list()
    try:
        while True:
            po = next(occurrences_gen)
            ids.append([po[2].payment_id, po[0].date()])
    except StopIteration:
        return ids


def get_future_payments():
    """
    Return ReccurentPayment in the current month
    :return: list of reccurrentpayment
    """

    return_list = list()
    for occ in PaymentOccurrence.objects.all():

        # get and format the last day of the month
        number_days_month = monthrange(datetime.date.today().year, datetime.date.today().month)[1]
        end_date = datetime.datetime.now() + datetime.timedelta(number_days_month - datetime.date.today().day)

        occurrence_gen = occ.all_occurrences(from_date=datetime.datetime.now(),
                                             to_date=end_date)

        data = process_occurrences(occurrence_gen)
        if data:
            for occurrence in data:
                payment = RecurrentPayment.objects.get(pk=occurrence[0])
                return_list.append([payment, occurrence[1]])

    return sorted(return_list, key=itemgetter(1))
