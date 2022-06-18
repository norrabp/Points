from flask import Flask, request, jsonify
from datetime import datetime
from time import mktime, strptime
import json
import operator
import collections

app = Flask(__name__)

Transactions = list()

PayerTotals = dict()


@app.route('/', methods=['GET'])
def index():
    return jsonify(Transactions)


@app.route('/points/add-transaction', methods=['POST'])
def addTransaction():
    points = int(request.json["points"])
    payer = request.json["payer"]
    if points < 0 and payer in PayerTotals and PayerTotals[payer] + points < 0:
        return jsonify({
            'Message': "Transaction would make payer points lets than 0",
            'payer': payer,
            'points': PayerTotals[payer]
        })
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
    if request.json["payer"] not in PayerTotals:
        PayerTotals[payer] = points
    else:
        PayerTotals[payer] += points
    
    Transactions.sort(key=lambda x: datetime.strptime(x['timestamp'], '%Y-%m-%dT%H:%M:%SZ'))
    return jsonify(Transactions)


@app.route('/points/payers', methods=['GET'])
def getPayers():
    return jsonify(PayerTotals)


@app.route('/points/use-points', methods=['Post'])
def spendPoints():
    points_to_spend = int(request.json["points"])
    total_points = sum(PayerTotals.values())
    spent_per_payer = dict()
    if total_points < points_to_spend:
        return jsonify({"message": "Not enough points to spend",
                        "totalPoints": total_points})
    for transaction in Transactions:
        if points_to_spend > 0:
            points_remaining = transaction['points_remaining']
            payer = transaction['payer']
            points_spent = 0
            if transaction["points_remaining"] < points_to_spend:
                points_spent = transaction['points_remaining']
                PayerTotals[payer] -= transaction['points_remaining']
                points_to_spend -= points_remaining
                transaction["points_remaining"] = 0
            else:
                points_spent = points_to_spend
                PayerTotals[payer] -= points_to_spend
                transaction["points_remaining"] -= points_to_spend
                points_to_spend = 0
            if payer not in spent_per_payer:
                spent_per_payer[payer] = -points_spent
            else:
                spent_per_payer[payer] -= points_spent
        else:
            break
    return jsonify(spent_per_payer)


if __name__ == "__main__":
    app.run(debug=True)
