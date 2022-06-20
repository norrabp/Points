from .. import PayerTotals


def spend_transaction_points(transaction, points_to_spend):
    """
    Spend points on the current transaction
    Arguments:
        transaction: The current transaction containg {
            payer: <the payer for the transactino>
            points_remaining: <number of points left to spend on this transaction>
        }
        points_to_spend: Number of points remaining to spend on the current spend call
    Returns:
        The number of points spent on this transactino
    """
    payer = transaction['payer']
    points_used = 0
    if transaction["points_remaining"] > 0:
        # Check if the total for the payer is less than the transaction
        # Occurs if there are negative transactions for that payer
        if PayerTotals[payer] >= transaction["points_remaining"]:
            # Spend transaction remaining points unless there are less points to spend
            if transaction["points_remaining"] < points_to_spend:
                points_used = transaction['points_remaining']
            else:
                points_used = points_to_spend
        else:
            # Spend total for the payer unless there are less points to spend
            if PayerTotals[payer] < points_to_spend:
                points_used = PayerTotals[payer]
            else:
                points_used = points_to_spend
        PayerTotals[payer] -= points_used
        transaction["points_remaining"] -= points_used
    return points_used
