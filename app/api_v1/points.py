from . import api
from .. import Transactions, PayerTotals
from ..exceptions import ValidationError
from ..core import core
from flask import jsonify, request
from datetime import datetime


@api.route('/transactions/', methods=['GET'])
def index():
    return jsonify(Transactions)


@api.route('/transactions/', methods=['POST'])
def add_transaction():
    try:
        points = int(request.json["points"])
        payer = request.json["payer"]
    except KeyError as e:
        raise ValidationError('Invalid request: missing ' + e.args[0])
    except TypeError as e:
        raise ValidationError('Invalid request: missing points and payer')
    if points < 0 and payer in PayerTotals and PayerTotals[payer] + points < 0:
        return jsonify({
            'message': "Transaction would make payer points lets than 0",
            'payer': payer,
            'payer_points': PayerTotals[payer]
        }), 200
    if "timestamp" in request.json:
        timestamp = request.json['timestamp']
    else:
        timestamp = datetime.strftime(datetime.utcnow(), '%Y-%m-%dT%H:%M:%SZ')
    Transactions.append({
        "timestamp": timestamp,
        "payer": payer,
        "points": points,
        "points_remaining": points
    })
    if payer not in PayerTotals:
        PayerTotals[payer] = points
    else:
        PayerTotals[payer] += points
    Transactions.sort(key=lambda x: datetime.strptime(x['timestamp'], '%Y-%m-%dT%H:%M:%SZ'))
    return jsonify(Transactions), 201


@api.route('/points/', methods=['GET'])
def get_payers():
    return jsonify(PayerTotals)


@api.route('/points/', methods=['POST'])
def spend_points():
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
    if total_points < points_to_spend:
        return jsonify({"message": "Not enough points to spend",
                        "totalPoints": total_points})
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

