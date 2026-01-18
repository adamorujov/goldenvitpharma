def is_payment_success(order):
    return order.get("status") == "Fully paid"


def normalize_status(status):
    return status.replace(" ", "_").upper()
