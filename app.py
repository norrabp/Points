from flask import Flask, request, jsonify
from datetime import datetime
from time import mktime, strptime
import json
import operator
import collections

app = Flask(__name__)

transactions = list()

payerTotals = dict()


@app.route('/', methods=['GET'])
def index():
    return jsonify(json.dumps(transactions))


@app.route('/points/add-transaction', methods=['POST'])
def addTransaction():
    if "timestamp" in request.json:
        timestamp = request.json['timestamp']
    else:
        timestamp = datetime.strftime(datetime.utcnow(), '%Y-%m-%dT%H:%M:%SZ')
    transactions.append({
        "timestamp": timestamp,
        "payer": request.json["payer"],
        "points": int(request.json["points"]),
        "pointsRemaining": int(request.json["points"])
    })
    if request.json["payer"] not in payerTotals:
        payerTotals[request.json["payer"]] = int(request.json["points"])
    else:
        payerTotals[request.json["payer"]] += int(request.json["points"])
    
    transactions.sort(key=lambda x: datetime.strptime(x['timestamp'], '%Y-%m-%dT%H:%M:%SZ'))
    return jsonify(transactions)


@app.route('/points/payers', methods=['GET'])
def getPayers():
    return jsonify(payerTotals)


@app.route('/points/use-points', methods=['Post'])
def spendPoints():
    return jsonify({})


if __name__ == "__main__":
    app.run(debug=True)
