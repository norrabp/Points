import unittest
from app import create_app, PayerTotals, Transactions
from ..utils import client,timestamp

class TestTransactions(unittest.TestCase):
    """
    Test cases involving adding transactions
    """
    def setUp(self):
        self.app = create_app('testing')
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.client = client.TestClient(self.app)

    def tearDown(self):
        PayerTotals.clear()
        Transactions.clear()
        self.ctx.pop()

    def test1Trans1Payer_1TransInResp(self):
        """
        Base case for adding a transaction, verify that the transaction is added
        and the info for all transactions are returned.
        """
        rv, json = self.client.post('/api/v1/transactions/', data={'payer': 'Fetch', 'points': 100})
        self.assertTrue(rv.status_code == 201)
        self.assertTrue(len(json) == 1)
        try:
            self.assertTrue(json[0]['payer'] == 'Fetch')
            self.assertTrue(json[0]['points'] == 100)
            self.assertTrue(json[0]['points_remaining'] == 100)
            self.assertTrue(Transactions[0]['payer'] == 'Fetch')
            self.assertTrue(Transactions[0]['points'] == 100)
            self.assertTrue(Transactions[0]['points_remaining'] == 100)
            self.assertTrue(PayerTotals['Fetch'] == 100)
        except KeyError as e:
            self.assertTrue(False, "Missing key " + e.args[0])
    
    def test3Trans2Payer_PayerPointsIsAccurate(self):
        """
        Test that the payer totals are accurately counted and stored
        """
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 100,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr()
        })
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 20,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr()
        })
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 200,
            'payer': 'Epic',
            'timestamp': timestamp.getTimestampStr()
        })
        rv, json = self.client.get('/api/v1/points/')
        try:
            self.assertTrue(json['Fetch'] == 120)
            self.assertTrue(json['Epic'] == 200)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])
        

    def test2Trans1Payer_SecondTransEarlier_SecondTransShowsFirst(self):
        """
        Test that if a transaction is posted with an earlier timestamp than another
        existing transaction that it is first in the order
        """
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 100,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr(2022,1,5,12,0,0)
        })
        second_instant = timestamp.getTimestampStr(2022,1,5,11,59,59)
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 20,
            'payer': 'Fetch',
            'timestamp': second_instant
        })
        rv, json = self.client.get('/api/v1/transactions/')
        self.assertTrue(len(json) == 2, "Number of transactions returned is " + str(len(json)) + " instead of 2")
        try:
            self.assertTrue(json[0]['timestamp'] == second_instant)
        except KeyError as e:
            self.assertTrue(False, "Missing key " + e.args[0])
