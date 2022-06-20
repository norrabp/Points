import unittest
from app import create_app, PayerTotals, Transactions
from ..utils import client,timestamp


class TestSpendNegative(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.client = client.TestClient(self.app)

    def tearDown(self):
        PayerTotals.clear()
        Transactions.clear()
        self.ctx.pop()

    def test2Trans1Payer1Spend_SpendGTSum_RespondNotEnough(self):
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 100,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr()
        })
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': -20,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr()
        })
        rv, json = self.client.post('/api/v1/points/', data={
            'points': 90
        })
        self.assertTrue('message' in json)

    def test2Trans1Payer1Spend_SpendLTSum_10Left(self):
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 100,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr()
        })
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': -20,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr()
        })
        rv, json = self.client.post('/api/v1/points/', data={
            'points': 70
        })
        try:
            self.assertTrue(json['Fetch'] == -70)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])
        rv, json = self.client.get('/api/v1/points/')
        try:
            self.assertTrue(json['Fetch'] == 10)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])

    def test3Trans2Payer1Spend_PayerWithNegLTSpend_OnlySecondPayerHasPoints(self):
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 100,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr()
        })
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': -20,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr()
        })
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 1000,
            'payer': 'Epic',
            'timestamp': timestamp.getTimestampStr()
        })
        rv, json = self.client.post('/api/v1/points/', data={
            'points': 200
        })
        try:
            self.assertTrue(json['Fetch'] == -80)
            self.assertTrue(json['Epic'] == -120)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])
        rv, json = self.client.get('/api/v1/points/')
        try:
            self.assertTrue(json['Fetch'] == 0)
            self.assertTrue(json['Epic'] == 880)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])

    def test4Trans2Payer1Spend_PayerWithNegGTSpend_OnlyFirstPayerHasPoints(self):
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 100,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr()
        })
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': -50,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr()
        })
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 50,
            'payer': 'Epic',
            'timestamp': timestamp.getTimestampStr()
        })
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 100,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr()
        })
        rv, json = self.client.post('/api/v1/points/', data={
            'points': 180
        })
        try:
            self.assertTrue(json['Fetch'] == -130)
            self.assertTrue(json['Epic'] == -50)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])
        rv, json = self.client.get('/api/v1/points/')
        try:
            self.assertTrue(json['Fetch'] == 20)
            self.assertTrue(json['Epic'] == 0)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])




