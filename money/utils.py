from money.models import Total


def compute_total(payments,categories):
    """
    Compute the total by category
    :param payments:
    :return: list of dict used by table to show data
              [ {column_label : column name }
    """
    total = []
    for category in categories:
        total_category = 0
        for payment in payments:
            if payment.category == category:
                total_category += float(payment.sum)

        total_obj = Total(category.name,format_number(total_category))
        total.append(total_obj)

    return total


def append_to_total(totals,totals_to_append,month_index):
    """
    Append one total object to another
    :param totals:
    :param totals_to_append:
    :param month_index:
    :return:
    """
    for total in totals:
        for total1 in totals_to_append:
            if total.categorie == total1.categorie:
                key = "total_prev_" + str(month_index)
                setattr(total,key,format_number(float(total1.total)))

def format_number(number):
    return "{:4.1f}".format(number)