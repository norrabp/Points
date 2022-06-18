from .. import PayerTotals


def spend_transaction_points(transaction, points_to_spend):
    payer = transaction['payer']
    points_used = 0
    if transaction["points_remaining"] > 0:
        if PayerTotals[payer] >= transaction["points_remaining"]:
            if transaction["points_remaining"] < points_to_spend:
                points_used = transaction['points_remaining']
            else:
                points_used = points_to_spend
        else:
            if PayerTotals[payer] < points_to_spend:
                points_used = PayerTotals[payer]
            else:
                points_used = points_to_spend
        PayerTotals[payer] -= points_used
        transaction["points_remaining"] -= points_used
    return points_used
