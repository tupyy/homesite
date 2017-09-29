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
        total_category_dict['suma'] = str(total_category)
        total.append(total_category_dict)

    return total