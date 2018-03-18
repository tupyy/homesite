import datetime
from django.core.management.base import BaseCommand, CommandError
from money.models import Payment, RecurrentPayment, PaymentOccurrence


class Command(BaseCommand):
    help = "Saves the recurrent payment which occurs today"

    def handle(self, *args, **options):
        for occ in PaymentOccurrence.objects.all():
            self.stdout.write("Looking for occurrences: " + occ.__str__())

            delta = datetime.timedelta(hours=12)
            occurrence_gen = occ.all_occurrences(from_date=datetime.datetime.now(),
                                                 to_date=datetime.datetime.now() + delta)

            for recurrent_id in self.process_occurrences(occurrence_gen):
                try:
                    payment = self.create_payment_instance(recurrent_id)
                    self.stdout.write("Saving payment instance: " + payment.__str__())
                except:
                    self.stderr.write(
                        "Cannot create instance of payment from recurrent payment id: " + str(recurrent_id))

    def process_occurrences(self, occurrences_gen):
        """
        For each occurrence return a list of payments id
        :param occurrences_gen:
        :return: list of payment id associated with the occurrences
        """

        ids = list()
        try:
            while True:
                po = next(occurrences_gen)
                ids.append(po[2].payment_id)
        except StopIteration:
            return ids

    def create_payment_instance(self, recurrent_payment_id):
        recurrent_payment = RecurrentPayment.objects.get(pk=recurrent_payment_id)
        payment = Payment.objects.create(contract=recurrent_payment.contract,
                                         category=recurrent_payment.category,
                                         subcategory=recurrent_payment.subcategory,
                                         date=datetime.datetime.today(),
                                         sum=recurrent_payment.sum,
                                         comments=recurrent_payment.comments,
                                         nb_tickete=0,
                                         user=recurrent_payment.user)
        return payment
