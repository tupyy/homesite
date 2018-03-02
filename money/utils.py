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
        total_category_dict = {}
        for payment in payments:
            if payment.category == category:
                total_category += float(payment.sum)

        total_category_dict['categorie'] = category.name
        total_category_dict['suma'] = total_category
        total.append(total_category_dict)

    return total


def append_to_total(totals,totals_to_append,month_index):
    for total in totals:
        for total1 in totals_to_append:
            if total['categorie'] == total1['categorie']:
                key = "suma_prev_" + str(month_index)
                total[key] = "{:4.1f}".format(total1['suma'])