from . import api
from .. import Transactions, PayerTotals
from ..exceptions import ValidationError
from ..core import core
from flask import jsonify, request
from datetime import datetime


@api.route('/transactions/', methods=['GET'])
def index():
    """ Return list of all transactions """
    return jsonify(Transactions)


@api.route('/transactions/', methods=['POST'])
def add_transaction():
    """ Adds a new transaction """
    # Verify correct input
    try:
        points = int(request.json["points"])
        payer = request.json["payer"]
    except KeyError as e:
        raise ValidationError('Invalid request: missing ' + e.args[0])
    except TypeError as e:
        raise ValidationError('Invalid request: missing points and payer')
    # If transaction negative and it makes the total points for a payer negative
    # do not add transaction
    if points < 0 and payer in PayerTotals and PayerTotals[payer] + points < 0:
        return jsonify({
            'message': "Transaction would make payer points lets than 0",
            'payer': payer,
            'payer_points': PayerTotals[payer]
        }), 200
    # If no timestamp sent, set timestamp to now
    if "timestamp" in request.json:
        timestamp = request.json['timestamp']
    else:
        timestamp = datetime.strftime(datetime.utcnow(), '%Y-%m-%dT%H:%M:%SZ')
    # Add transaction
    Transactions.append({
        "timestamp": timestamp,
        "payer": payer,
        "points": points,
        "points_remaining": points
    })
    # Increse total for payer
    if payer not in PayerTotals:
        PayerTotals[payer] = points
    else:
        PayerTotals[payer] += points
    # Sort transactions by timestamp
    Transactions.sort(key=lambda x: datetime.strptime(x['timestamp'], '%Y-%m-%dT%H:%M:%SZ'))
    return jsonify(Transactions), 201


@api.route('/points/', methods=['GET'])
def get_payers():
    """ Returns the total number of points per payer """
    return jsonify(PayerTotals)


@api.route('/points/', methods=['POST'])
def spend_points():
    """ Spend points starting with the earliest transaction"""
    # Validate input
    try:
        points_to_spend = int(request.json["points"])
    except KeyError as e:
        raise ValidationError('Invalid request: missing ' + e.args[0])
    except TypeError as e:
        raise ValidationError('Invalid request: missing points')
    if points_to_spend < 0:
        raise ValidationError('Invalid request: points must not be negative')
    total_points = sum(PayerTotals.values())
    spent_per_payer = dict()
    # Verify there are enough points to spend
    if total_points < points_to_spend:
        return jsonify({"message": "Not enough points to spend",
                        "totalPoints": total_points})
    # Spend points and update payer totals
    for transaction in Transactions:
        if points_to_spend > 0:
            points_used = core.spend_transaction_points(transaction, points_to_spend)
            points_to_spend -= points_used
            payer = transaction['payer']
            if payer not in spent_per_payer:
                spent_per_payer[payer] = -points_used
            else:
                spent_per_payer[payer] -= points_used
        else:
            break
    return jsonify(spent_per_payer), 201

