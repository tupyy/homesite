from django.db import models

from django.contrib.auth.models import User

class RevenueManager(models.Manager):
    """
    Mananger to compute the total revenu
    """

    def total(self):
        total_revenue = 0
        revenues = Revenue.objects.all()
        for revenue in revenues:
            total_revenue += revenue.sum

        return total_revenue


class Revenue(models.Model):
    """
    Model for the revenus
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    sum = models.DecimalField(max_digits=8, decimal_places=2)

    # set managers
    objects = models.Manager()
    total = RevenueManager()

    def __str__(self):
        return "Revenue {}".format(self.user.__str__().title())
